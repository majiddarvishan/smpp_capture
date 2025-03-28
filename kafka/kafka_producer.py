from kafka import KafkaProducer
import json

KAFKA_BROKER = "localhost:9092"

producer = KafkaProducer(
    bootstrap_servers=[KAFKA_BROKER],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(topic, data):
    """Send parsed SMPP data to Kafka."""
    producer.send(topic, data)
    producer.flush()
