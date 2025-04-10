### This file contains some project related commands

Run in exec of broker to check topic produced.

`kafka-topics --list --bootstrap-server broker:29092`


To get all the data per topic - vehicle_data:

`kafka-console-consumer --topic vehicle_data --bootstrap-server broker:9092 --from-beginning`


Clearing residual data:

`kafka-topics --delete --topic gps_data emergency_data --bootstrap-server broker:29092`

```
kafka-topics --delete --topic gps_data --bootstrap-server broker:29092
kafka-topics --delete --topic vehicle_data --bootstrap-server broker:29092
kafka-topics --delete --topic emergency_data --bootstrap-server broker:29092
kafka-topics --delete --topic traffic_data --bootstrap-server broker:29092
kafka-topics --delete --topic weather_data --bootstrap-server broker:29092
```

### Dlt

`dlt pipeline -v <pipeline_name> info`

`dlt pipeline drop --drop-all`

`dlt pipeline drop <resource_name>`

`dlt pipeline drop --state-paths`

Submitting jobs to spark

```
docker exec -it smart-city-spark-master-1 spark-submit \
--master spark://spark-master:7077 \
--packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,\
org.apache.hadoop:hadoop-aws:3.3.4,\
com.amazonaws:aws-java-sdk-bundle:1.12.316 \
jobs/spark-city.py
```




