import json
import uuid
from typing import Dict, Any, Optional
from confluent_kafka import SerializingProducer, Message

class KafkaProducerManager:
    """Handles Kafka data production."""
    def __init__(self, producer_config: Dict[str, Any]) -> None:
        """
        Initializes the KafkaProducerManager with the given producer configuration.

        """
        self.producer = SerializingProducer(producer_config)

    def produce_data(self, topic: str, data: Dict[str, Any]) -> None:
        """Produces a message to the Kafka topic."""
        self.producer.produce(
            topic,
            key=str(data['id']),
            value=json.dumps(data, default=self.json_serializer).encode('utf-8'),
            on_delivery= self.delivery_report
        )
        self.producer.flush()

    def json_serializer(self, obj: Any) -> str:
        if isinstance(obj, uuid.UUID):
            return str(obj)
        raise TypeError(f"Object of type {obj.__class__.__name__} is not JSOn serializable")

    @staticmethod
    def delivery_report(err: Optional[str], msg: Message) -> None:
        """Handles delivery reports for Kafka messages."""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
