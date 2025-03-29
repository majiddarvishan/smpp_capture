from kafka import KafkaProducer, KafkaConsumer
import json
import logging

from config.logging_config import get_logger

logger = get_logger(__name__)

# Kafka Configuration
KAFKA_BROKER = "localhost:9092"  # Change to your broker address
SMPP_TOPIC = "smpp_packets"
ALERTS_TOPIC = "smpp_alerts"
GROUP_ID = "smpp_consumer_group"

def get_kafka_producer():
    """Creates and returns a Kafka producer."""
    try:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BROKER,
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
            acks="all",
            retries=5,
        )
        logger.info("✅ Kafka producer connected successfully.")
        return producer
    except Exception as e:
        logger.error(f"❌ Kafka producer connection failed: {e}")
        return None


def get_kafka_consumer(topic=SMPP_TOPIC, group_id=GROUP_ID, auto_offset_reset="earliest"):
    """Creates and returns a Kafka consumer."""
    try:
        consumer = KafkaConsumer(
            topic,
            bootstrap_servers=KAFKA_BROKER,
            group_id=group_id,
            auto_offset_reset=auto_offset_reset,
            enable_auto_commit=True,
            value_deserializer=lambda v: json.loads(v.decode("utf-8")),
        )
        logger.info(f"✅ Kafka consumer connected to topic '{topic}'.")
        return consumer
    except Exception as e:
        logger.error(f"❌ Kafka consumer connection failed: {e}")
        return None
