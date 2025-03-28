# 📌 Setting Up Kibana Dashboard

1. Start Elasticsearch & Kibana

```bash
sudo systemctl start elasticsearch
sudo systemctl start kibana
```

2. Index Pattern in Kibana

* Open Kibana (http://localhost:5601)
* Go to Stack Management → Index Patterns
* Create index pattern: smpp_submit_sm_live
* Add fields: source_addr, destination_addr, short_message, sequence_number, etc.

3. Create Dashboard

* Go to Dashboard → Create New Dashboard
* Add Visualizations:
    - Bar Chart: Count of SMPP messages by source
    - Line Chart: SMPP message rate over time
    - Table: Raw Submit_SM message logs



# 🚀 How to Run?

## Option 1: Live Capture Mode

```bash
python main.py --mode live
```

# Option 2: Read from PCAP File

```bash
python main.py --mode pcap --file path/to/your.pcap
```


# 🔷 Step-by-Step Kafka Integration

## 🛠 Step 1: Install Kafka & Dependencies
First, install the Kafka Python client:

```bash
pip install kafka-python
```

Ensure Kafka & Zookeeper are running:

```bash
bin/zookeeper-server-start.sh config/zookeeper.properties
bin/kafka-server-start.sh config/server.properties
```

Create topics:

```bash
bin/kafka-topics.sh --create --topic smpp-submit --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
bin/kafka-topics.sh --create --topic smpp-deliver --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
bin/kafka-topics.sh --create --topic smpp-response --bootstrap-server localhost:9092 --partitions 3 --replication-factor 1
```

🔷 Step 1: Kafka & Spark Streaming for SMPP Analytics
📌 Architecture Overview
1️⃣ Kafka Producers (from packet capture) send data to Kafka.
2️⃣ Spark Streaming consumes Kafka topics and processes SMPP analytics.
3️⃣ Processed data is sent to Elasticsearch for storage & visualization.
4️⃣ Kafka Streams detects high-latency Submit/Submit-Resp pairs.

🔷 Step 2: Kafka Streams for Latency Alerting
If Submit-Resp latency exceeds a threshold, send an alert.
✅ Continuously monitors latency & triggers alerts.
✅ Integrate with Slack, Email, or Webhooks for alerting.

🔷 Step 3: Grafana + Elasticsearch for Real-Time Dashboards
1. Install Grafana + Elasticsearch

2. Configure Grafana Datasource

- Go to Grafana → Configuration → Data Sources
- Add Elasticsearch (http://elasticsearch:9200)

3. Create Dashboard with Panels
- Latency Panel: avg(latency) by sequence_number
- Error Panel: count(command_status != 0)

✅ Grafana provides a live view of SMPP performance.

2️⃣ Test Endpoints
Get latency:
```bash
curl http://localhost:8000/latency/12345
```

Get high latency (above 500ms):
```bash
curl http://localhost:8000/high-latency?min_latency=500
```

Get errors:
```bash
curl http://localhost:8000/errors
```

Get raw packet:
```bash
curl http://localhost:8000/packet/1
```

```graphql
smpp_monitoring/
│── 📂 config/            # Configuration files (logging, database, etc.)
│   │── config.py         # Environment variables, PostgreSQL & Kafka settings
│   │── logging_config.py # Logging setup
│
│── 📂 database/          # PostgreSQL database interactions
│   │── db.py             # Database connection & setup
│   │── queries.py        # SQL queries for inserting & fetching data
│
│── 📂 smpp/              # SMPP packet processing
│   │── smpp_processor.py # Extract and analyze SMPP packets
│   │── packet_parser.py  # Parse Submit_SM, Submit_SM_RESP, Deliver_SM, etc.
│   │── pcap_reader.py    # Read from PCAP files
│   │── packet_sniffer.py # Live network capture
│
│── 📂 kafka/             # Kafka Integration
│   │── producer.py       # Push SMPP packet data to Kafka
│   │── consumer.py       # Process Kafka messages in Spark
│   │── kafka_config.py   # Kafka settings
│
│── 📂 analytics/         # Spark analytics for latency detection
│   │── spark_processor.py  # Spark job for real-time analytics
│   │── alerting.py       # Kafka Streams for high-latency alerts
│
│── 📂 api/               # REST API for querying SMPP insights
│   │── api.py            # FastAPI for serving insights
│   │── models.py         # Data models (Pydantic)
│   │── routes/           # API endpoints
│       │── smpp_routes.py  # SMPP-specific routes
│       │── healthcheck.py  # Health check endpoints
│
│── 📂 dashboards/        # Visualization with Grafana
│   │── grafana_config/   # Grafana dashboards & queries
│
│── 📂 tests/             # Unit & integration tests
│   │── test_db.py        # Test database queries
│   │── test_parser.py    # Test SMPP parsing
│   │── test_api.py       # Test API responses
│
│── Dockerfile            # Docker configuration
│── docker-compose.yml    # Multi-service container orchestration
│── requirements.txt      # Python dependencies
│── README.md             # Project documentation
```