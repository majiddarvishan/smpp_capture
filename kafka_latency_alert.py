from kafka import KafkaConsumer
import json

KAFKA_BROKER = "localhost:9092"
LATENCY_ALERT_TOPIC = "smpp-latency-alerts"
LATENCY_THRESHOLD_MS = 500  # Alert if >500ms

def check_latency():
    """Monitors SMPP latency and sends alerts if too high."""
    consumer = KafkaConsumer(
        "smpp-submit-response-latency",
        bootstrap_servers=[KAFKA_BROKER],
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )

    for message in consumer:
        latency = message.value["latency"]
        sequence_number = message.value["sequence_number"]

        if latency > LATENCY_THRESHOLD_MS:
            alert_msg = f"⚠️ High latency detected! Seq: {sequence_number}, Latency: {latency} ms"
            print(alert_msg)
            # Send to alerting system (email, webhook, etc.)

if __name__ == "__main__":
    check_latency()
