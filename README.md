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

