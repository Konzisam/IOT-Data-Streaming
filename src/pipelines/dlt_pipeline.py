import json
import dlt
import logging
from typing import Any, Dict
from confluent_kafka import Message
from src.kafka import kafka_consumer
from ..models.schema import (
    VehicleModel, GPSModel, TrafficModel, WeatherModel, EmergencyModel
)

logging.basicConfig(level=logging.DEBUG, format='[%(levelname)s] %(message)s')

TOPIC_SCHEMA_MAP = {
    "vehicle_data": VehicleModel,
    "gps_data": GPSModel,
    "traffic_data": TrafficModel,
    "weather_data": WeatherModel,
    "emergency_data": EmergencyModel,
}


def msg_processor_with_validation(msg: Message) -> Dict[str, Any]:
    topic = msg.topic()

    if topic not in TOPIC_SCHEMA_MAP:
        raise ValueError(f"Unknown topic: {topic}")

    raw_message = msg.value().decode("utf-8")
    payload = json.loads(raw_message)

    schema = TOPIC_SCHEMA_MAP[topic]

    try:
        validated = schema(**payload)
        record = validated.dict()
        # Grouping Kafka metadata under a single '_kafka' key
        record["_kafka"] = {
            "topic": topic,
            "key": msg.key().decode("utf-8") if msg.key() else None,
            "partition": msg.partition(),
        }

        return record

    except Exception as e:
        logging.error(f"Validation failed for topic {topic}: {e}")
        return {}


def run_kafka_ingestion():
    pipeline = dlt.pipeline(
        pipeline_name="iot_service",
        destination="snowflake",
        dataset_name="iot_stream"
    )

    topics = list(TOPIC_SCHEMA_MAP.keys())
    logging.info(f"Subscribing to topics: {topics}")

    try:
        logging.info("Fetching a new batch of data from Kafka...")
        data = kafka_consumer(
            topics=topics,
            msg_processor=msg_processor_with_validation,
            batch_size=3000,
            batch_timeout=3,
        )


        if data:
            load_info = pipeline.run(data, write_disposition="append") # adjust accordingly
            if not load_info.load_packages:
                logging.warning("No data was loaded — load_packages is empty.")
            else:
                logging.info(f"Pipeline run completed. Loaded {len(load_info.load_packages)} package(s).")
        else:
            logging.warning("No data received in this batch.")

    except Exception as e:
        logging.exception("Pipeline run failed.")

    logging.info("No more data to process. Exiting.")


if __name__ == "__main__":
    run_kafka_ingestion()
