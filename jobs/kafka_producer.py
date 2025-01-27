import json
from typing import Dict, Any, Optional
from confluent_kafka import SerializingProducer, Message

class KafkaProducerManager:
    """Handles Kafka data production."""
    def __init__(self, producer_config: Dict[str, Any]) -> None:
        """
        Initializes the KafkaProducerManager with the given producer configuration.

        :param producer_config: Configuration dictionary for SerializingProducer.
        """
        self.producer = SerializingProducer(producer_config)

    def produce_data(self, topic: str, data: Dict[str, Any]) -> None:
        """Produces a message to the Kafka topic."""
        self.producer.produce(
            topic,
            key=str(data['id']),
            value=json.dumps(data).encode('utf-8'),
            on_delivery=lambda err, msg: print(
                f"Delivery error: {err}" if err else f"Delivered: {msg.topic()}"
            )
        )
        self.producer.flush()

    @staticmethod
    def delivery_report(err: Optional[str], msg: Message) -> None:
        """Handles delivery reports for Kafka messages."""
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
