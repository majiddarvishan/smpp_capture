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
