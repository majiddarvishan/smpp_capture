from kafka import KafkaConsumer, KafkaProducer
import json
import logging
import time
from config.kafka_config import KAFKA_BROKER, SMPP_TOPIC, ALERTS_TOPIC
from config.logging_config import get_logger

logger = get_logger(__name__)

# Define alert thresholds (adjust as needed)
LATENCY_THRESHOLD_MS = 500  # Alert if latency > 500ms
HIGH_LATENCY_COUNT_THRESHOLD = 5  # Alert if 5+ high-latency packets occur within a window
ALERT_WINDOW_SECONDS = 60  # Monitoring window (in seconds)

# Kafka producer for sending alerts
producer = KafkaProducer(
    bootstrap_servers=KAFKA_BROKER,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)

# Kafka consumer for reading latency data
consumer = KafkaConsumer(
    SMPP_TOPIC,
    bootstrap_servers=KAFKA_BROKER,
    group_id="alerting_group",
    auto_offset_reset="latest",
    enable_auto_commit=True,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
)

logger.info("✅ Alerting system started.")

# Track high-latency packets within the time window
high_latency_records = []


def send_alert(alert_message):
    """Sends alert to Kafka and logs it."""
    alert_data = {
        "timestamp": int(time.time() * 1000),
        "alert_message": alert_message,
    }

    producer.send(ALERTS_TOPIC, alert_data)
    producer.flush()
    logger.warning(f"🚨 ALERT: {alert_message}")


# Process Kafka messages
for msg in consumer:
    packet = msg.value
    latency_ms = packet.get("latency_ms", 0)
    sequence_number = packet.get("sequence_number", None)

    if latency_ms > LATENCY_THRESHOLD_MS:
        high_latency_records.append({"time": time.time(), "sequence_number": sequence_number, "latency": latency_ms})
        logger.warning(f"⚠️ High latency detected: {latency_ms}ms (Seq: {sequence_number})")

    # Remove old records outside the time window
    high_latency_records = [record for record in high_latency_records if time.time() - record["time"] < ALERT_WINDOW_SECONDS]

    # Trigger alert if too many high-latency packets
    if len(high_latency_records) >= HIGH_LATENCY_COUNT_THRESHOLD:
        send_alert(f"⚡ High latency detected! {len(high_latency_records)} packets > {LATENCY_THRESHOLD_MS}ms in {ALERT_WINDOW_SECONDS}s")
        high_latency_records.clear()  # Reset tracking after alert
