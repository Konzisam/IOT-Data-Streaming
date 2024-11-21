Run in exec of broker to check topic produced.\
`kafka-topics --list --bootstrap-server broker:29092`\

To get all the data:\
`kafka-console-consumer --topic vehicle_data --bootstrap-server broker:9092 --from-beginning`

clearing residual data:
topics:\ 
* gps_data
* vehicle _data
* emergency_data
* traffic_data
* weather_data

`kafka-topics --delete --topic gps_data emergency_data --bootstrap-server broker:29092`

Submitting jobs:\
`docker exec -it smart-city-spark-master-1 spark-submit \
--master spark://spark-master:7077 \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,\
org.apache.hadoop:hadoop-aws:3.3.4,\
com.amazonaws:aws-java-sdk-bundle:1.12.316 \
jobs/spark-city.py
`










docker exec -it smart-city-spark-master-1 bash
ls /opt/bitnami/spark/jars/ | grep aws

docker exec -it smart-city-spark-master-1 spark-submit --master spark://spark-master:7077 \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.3 \
  jobs/spark-city.py

