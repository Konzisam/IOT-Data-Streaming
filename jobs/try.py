from pyspark.sql import SparkSession
from pyspark.sql import Row

# Initialize Spark session
spark = SparkSession.builder.appName("S3 Test").getOrCreate()

# Create a sample dataframe
data = [
    Row(id=1, device_Id="device1", timestamp="2024-11-21 01:23:45", location="location1", speed=60, direction="North", make="Toyota", model="Corolla", year=2020, fuelType="Petrol"),
    Row(id=2, device_Id="device2", timestamp="2024-11-21 01:24:45", location="location2", speed=50, direction="South", make="Honda", model="Civic", year=2021, fuelType="Diesel")
]

df = spark.createDataFrame(data)

# Save as Parquet file (or CSV if preferred)
df.write.parquet("/tmp/sample_vehicle_data.parquet")

# Or save as CSV if preferred:
# df.write.csv("/tmp/sample_vehicle_data.csv")
