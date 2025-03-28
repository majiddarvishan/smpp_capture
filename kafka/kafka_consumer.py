from kafka import KafkaConsumer
from database.elasticsearch_client import store_in_elasticsearch, update_command_status
import json
import threading

KAFKA_BROKER = "localhost:9092"

def create_consumer(topic):
    """Creates a Kafka consumer for a given topic."""
    return KafkaConsumer(
        topic,
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

def process_submit_sm():
    """Processes Submit_SM packets from Kafka and stores them in Elasticsearch."""
    consumer = create_consumer("smpp-submit")
    for message in consumer:
        store_in_elasticsearch(message.value)

def process_submit_resp():
    """Processes Submit_SM_RESP packets and updates Elasticsearch."""
    consumer = create_consumer("smpp-response")
    for message in consumer:
        update_command_status(
            message.value["sequence_number"],
            message.value["command_status"],
            message.value["response_time_ms"],
            message.value["message_type"]
        )

def process_deliver_sm():
    """Processes Deliver_SM packets and stores them in Elasticsearch."""
    consumer = create_consumer("smpp-deliver")
    for message in consumer:
        store_in_elasticsearch(message.value)

if __name__ == "__main__":
    # Run consumers in parallel
    threading.Thread(target=process_submit_sm, daemon=True).start()
    threading.Thread(target=process_submit_resp, daemon=True).start()
    threading.Thread(target=process_deliver_sm, daemon=True).start()
