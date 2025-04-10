from src.config import configuration
from legacy.spark_streaming import SparkStreamingManager

# Kafka and S3 Configuration

S3_CONFIG = {
    "AWS_ACCESS_KEY": configuration.get("AWS_ACCESS_KEY"),
    "AWS_SECRET_KEY": configuration.get("AWS_SECRET_KEY"),
}

def spark_consumer() -> None:
    # Initialize Spark Streaming Manager
    spark_manager = SparkStreamingManager(kafka_servers='broker:29092', s3_config=S3_CONFIG)

    vehicle_stream = spark_manager.read_kafka_topic('vehicle_schema').alias('vehicle_stream')
    # gps_stream = spark_manager.read_kafka_topic('gps_schema').alias('gps_stream')
    traffic_stream = spark_manager.read_kafka_topic('traffic_schema').alias('traffic_stream')
    weather_stream = spark_manager.read_kafka_topic('weather_schema').alias('weather_stream')
    emergency_stream = spark_manager.read_kafka_topic('emergency_schema').alias('emergency_stream')

    print(vehicle_stream.isStreaming)
    vehicle_stream.printSchema()
    # gps_stream.printSchema()

    # Write streams to S3
    query1 = spark_manager.stream_writer(vehicle_stream,
                               "s3a://streaming-spark/checkpoints/vehicle_data",
                               "s3a://streaming-spark/data/vehicle_data")
    # query2 = spark_manager.stream_writer(gps_stream,
    #                            "s3a://streaming-spark/checkpoints/gps_data",
    #                            "s3a://streaming-spark/data/gps_data")
    query3 = spark_manager.stream_writer(traffic_stream,
                               "s3a://streaming-spark/checkpoints/traffic_data",
                               "s3a://streaming-spark/data/traffic_data")
    query4 = spark_manager.stream_writer(weather_stream,
                               "s3a://streaming-spark/checkpoints/weather_data",
                               "s3a://streaming-spark/data/weather_data")
    query5 = spark_manager.stream_writer(emergency_stream,
                               "s3a://streaming-spark/checkpoints/emergency_data",
                               "s3a://streaming-spark/data/emergency_data")

    queries = [query1, query3, query4, query5]
    for query in queries:
        if query:
            query.awaitTermination()
        else:
            print("Failed to start query.")

# Call the function to start consuming streams
if __name__ == "__main__":
    spark_consumer()
