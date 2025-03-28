# ELASTICSEARCH_HOST = "http://localhost:9200"
# INDEX_NAME = "smpp_submit_sm_live"
# SMPP_PORT = 2775  # SMPP Default Port

import os

POSTGRES_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB", "smpp"),
    "user": os.getenv("POSTGRES_USER", "user"),
    "password": os.getenv("POSTGRES_PASSWORD", "password"),
    "host": os.getenv("POSTGRES_HOST", "localhost"),
    "port": 5432
}

KAFKA_CONFIG = {
    "bootstrap_servers": os.getenv("KAFKA_SERVERS", "localhost:9092"),
    "smpp_topic": "smpp_packets"
}
