import json
import logging
from confluent_kafka import Producer

logger = logging.getLogger(__name__)

class KafkaProducerClient:
    def __init__(self):
        self.producer = Producer({
            "bootstrap.servers": "localhost:9095,localhost:9097,localhost:9102"
        })

    def publish(self, topic: str, data: dict):
        try:
            self.producer.produce(
                topic=topic,
                value=json.dumps(data).encode("utf-8"),
                key=str(data.get("id"))
            )
            self.producer.flush()
            logger.info(f"Event published - {topic}")
        except Exception as e:
            logger.error(f"Kafka publish error: {e}")

kafka_producer = KafkaProducerClient()
