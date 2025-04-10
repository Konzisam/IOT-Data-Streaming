from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, from_json
from typing import Dict
from legacy.schemas import SchemaManager

class SparkStreamingManager:
    """Handles Pyspark Streaming Logic."""
    def __init__(self, kafka_servers: str, s3_config: Dict[str,str], log_level: str = 'WARN') -> None:
        self.spark = ((SparkSession.builder.appName('SmartCityStreaming'))
             .config('spark.jars.packages',
                     "org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,"
                     'org.apache.hadoop:hadoop-aws:3.3.4,'
                     'com.amazonaws:aws-java-sdk-bundle:1.12.262')
             .config('spark.hadoop.fs.s3a.impl','org.apache.hadoop.fs.s3a.S3AFileSystem')
             .config('spark.hadoop.fs.s3a.access.key', s3_config.get('AWS_ACCESS_KEY'))
             .config('spark.hadoop.fs.s3a.secret.key', s3_config.get('AWS_SECRET_KEY'))
             .config('spark.hadoop.fs.s3a.aws.credentials.provider',
                     'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')
             .config('spark.hadoop.fs.s3a.endpoint', 's3.amazonaws.com')
             .getOrCreate())

        self.spark.sparkContext.setLogLevel(log_level)

        self.kafka_servers: str = kafka_servers

    def read_kafka_topic(self, topic: str) -> DataFrame:
        """Reads data from a Kafka topic and applies the schema."""
        schema = SchemaManager.get_schema(topic)
        if not schema:
            raise ValueError(f"No schema defined for topic: {topic}")

        return (self.spark.readStream
                .format('kafka')
                .option('kafka.bootstrap.servers', self.kafka_servers)
                .option('subscribe', topic)
                .option('startingOffsets', 'earliest')
                .load()
                .selectExpr('CAST(value as STRING)')
                .select(from_json(col('value'), schema).alias('data'))
                .select('data.*')
                .withWatermark('timestamp', delayThreshold='2 minutes'))

    def stream_writer(self, dataframe, checkpoint_path: str, output_path: str):
        """Writes data to S3 in Parquet format with streaming and checkpointing"""
        try:
            query = dataframe.writeStream \
                .format('parquet') \
                .option('checkpointLocation', checkpoint_path) \
                .option('path', output_path) \
                .outputMode('append') \
                .trigger(processingTime='4 minute') \
                .start()

            if query:
                print(f"Stream query started for {output_path}")
            else:
                print(f"Failed to start stream query for {output_path}")

            return query
        except Exception as e:
            print(f"Error starting stream for {output_path}: {e}")
            return None
