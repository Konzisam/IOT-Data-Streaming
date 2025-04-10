## 🛻 IOT Data Streaming with Kafka, DuckDB, dlt & Snowflake
This project simulates connected vehicles streaming real-time IoT data, including GPS, weather, traffic incidents, and emergency alerts, all while following real-world routes. 

The data is sent to Kafka topics, enabling downstream analytical processing for optimization. This allows for efficient data handling and real-time insights.

Data Architechture

(https://github.com/Konzisam/IOT-Data-Streaming/blob/master/assets/architechture.png?raw=true)


### 🌐 Overview
In the context of connected vehicles, real-time IoT data must be efficiently captured and processed for analytics. In this case we have vehicle data;

🚘 Vehicle Data

📍 GPS coordinates

🚦 Traffic camera events

🌤️ Weather conditions

🚨 Emergency alerts

 The goal is to demonstrate how to stream and analyze this data in real-time to improve decision-making, optimize route planning, and enhance fleet management.

By utilizing Apache Kafka for data streaming, DuckDB for fast, local analytics, and Snowflake for scalable cloud storage, this approach ensures that streaming data is efficiently captured and processed.

The vehicle routes are based on real geographical paths using the **OpenRouteService API**.

⚙️ **Tech Stack**

| Layer       | Technology                   | Purpose                                                 |
|-------------|------------------------------|---------------------------------------------------------|
| 💡 Simulation | Python, OpenRouteService API | Generate real-world vehicle data                        |
| 📡 Streaming  | Apache Kafka                 | Publish sensor data in real time                        |
| 🧠 Storage    | DuckDB, Snowflake            | Stage and analyze structured data loccally and in prod) |
| 🔁 Pipeline   | DLT (Data Loading Tool)      | Consuming and loading data to DUCKDB/Snowflake          |
| 🧪 Testing    | Pytest                       | Validate generation + Kafka flow                        |


## 🧭 How It Works
1. Simulated vehicles move between cities (e.g. Potsdam → Leipzig).

2. They emit various IoT-style data streams:

3. DLT listens to Kafka, and loads batched data when run into:

✅ DuckDB (local analytical DB for local testing)

✅ Snowflake (cloud warehouse - production setup)

## 🚀 To replicate the project
1. Clone the repo
```
git clone https://github.com/your-name/iot-data-streaming.git
cd iot-data-streaming
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Configure environment
```
AWS_ACCESS_KEY_ID=''
AWS_SECRET_ACCESS_KEY=''
OPENROUTE_KEY=''

SOURCES__KAFKA__CREDENTIALS__BOOTSTRAP_SERVERS="localhost:9092"
SOURCES__KAFKA__CREDENTIALS__GROUP_ID=""
SOURCES__KAFKA__CREDENTIALS__SECURITY_PROTOCOL="PLAINTEXT"
SOURCES__KAFKA__CREDENTIALS__SASL_MECHANISMS="PLAIN"
SOURCES__KAFKA__CREDENTIALS__SASL_USERNAME=""
SOURCES__KAFKA__CREDENTIALS__SASL_PASSWORD=""

DESTINATION__SNOWFLAKE__CREDENTIALS__DATABASE=""
DESTINATION__SNOWFLAKE__CREDENTIALS__PASSWORD=""
DESTINATION__SNOWFLAKE__CREDENTIALS__USERNAME=""
DESTINATION__SNOWFLAKE__CREDENTIALS__HOST=""
DESTINATION__SNOWFLAKE__CREDENTIALS__WAREHOUSE=""
DESTINATION__SNOWFLAKE__CREDENTIALS__ROLE=""
```

4. Start Kafka and Zookeeper using Docker Compose:
```
docker-compose up -d
```
This will bring up the Kafka and Zookeeper containers.Kafka broker will be available on localhost:9093.

5. There are two steps in starting the production and consumption of data:

✅ Running the simulation for kafka to produce the data

```python -m src.simulation.main```

✅ Running dlt to consume from kafka and write to duckDb/Snowflake. 

```python -m src.pipelines.dlt_pipelines```

If  running with DuckDB, an iot_service.duckdb file will be created in the root directory, allowing for querying using a tool like DBeaver.

_dlt consumes the data with an append strategy to the database. The idea is to have a scenario whereby the data streams continously and dlt is run on a schedule._

📁 Project Structure
```
.
├── docker-compose.yaml          # Optional: Start Kafka/Zoo locally
├── iot_service.duckdb           # Local DuckDB file (DLT writes here- may not exist before run)
├── replicate.md                 # Setup instructions for running locally
├── requirements.txt             # Python dependencies
├── README.md                    # Project overview and usage
│
├── src/                         # Main project source code
│   ├── config/                  # Env vars, API keys, ORS token, etc.
│   │   └── config.py
│   │
│   ├── kafka/                   # dlt-kafka helper functions
│   │   └── helpers.py
│   │
│   ├── models/                  # Pydantic typed schemas (vehicle, gps, etc.)
│   │   └── schema.py
│   │
│   ├── pipelines/               # DLT pipelines
│   │   └── dlt_pipeline.py      # Ingests from Kafka → DuckDB → Snowflake
│   │
│   ├── simulation/              # Vehicle & sensor simulators
│   │   ├── constants.py         # Enum: fuel types, etc.
│   │   ├── generators.py        # Sensor data generators (GPS, traffic, weather, etc.)
│   │   ├── kafka_producer.py    # Kafka producer manager
│   │   ├── main.py              # Entry point: run vehicle simulation
│   │   └── utils.py             # ORS helper client
│
├── tests/                       # Pytest-based unit tests
│   ├── test_Kafka_producer.py
│   ├── test_generators.py
│   ├── conftest.py              # Test fixtures
│
├── legacy/                      # Deprecated Spark pipeline code (not used) 
│   ├── spark_streaming.py       
│   ├── schemas.py
│   └── main.py

```
## Key Learnings:
1. Simplified Data Pipeline with DLT and Kafka:

- Switching from Spark to DLT simplified the pipeline. The is no longer need to manage Spark workers, and schema evolution is handled automatically.

2. Efficient Local Analytics with DuckDB:

-  DuckDB enables fast, local analytics without the need for additional infrastructure. It processes large datasets efficiently, reducing both setup time and costs.

3. Seamless Integration with Snowflake:

- dlt integrates well with Snowflake for scalable cloud storage, enabling smooth data transfers and analytics at scale(ofcourse with proper setup).

4. Non-Normalized Data Handling:

- DLT allows me to store non-normalized IoT data when needed, making it easier to keep related data in a single table.


## Summary:
- The integration of **DLT** for real-time data processing, **DuckDB** for efficient local analytics, and **Snowflake** for scalable cloud storage has streamlined the data pipeline. 

- The switch to Snowflake DB is seamless with DLT, allowing easy data loading and management without complex configurations. 

- This setup reduces infrastructure complexity whi

## Areas for Improvement:
- **Using an Orchestrator to Run DBT Models:** Incorporating an orchestrator like Airflow or Prefect could automate the scheduling and execution of DBT models, improving the overall pipeline management and reliability.

- **Infrastructure as Code (IaC) for Snowflake Provisioning:** Adopting IaC tools like Terraform to provision Snowflake resources could ensure consistency, scalability, and easier management of cloud infrastructure.