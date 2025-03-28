from fastapi import FastAPI, Query
from elasticsearch import Elasticsearch
from typing import List, Optional

# Initialize FastAPI
app = FastAPI(title="SMPP Insights API")

# Connect to Elasticsearch
ELASTICSEARCH_HOST = "http://elasticsearch:9200"
es = Elasticsearch([ELASTICSEARCH_HOST])

@app.get("/")
def home():
    return {"message": "Welcome to SMPP Insights API"}

@app.get("/latency/{sequence_number}")
def get_latency(sequence_number: str):
    """Get Submit-Resp latency for a specific sequence number"""
    query = {"query": {"match": {"sequence_number": sequence_number}}}
    result = es.search(index="smpp-latency", body=query)
    if result["hits"]["total"]["value"] > 0:
        return result["hits"]["hits"][0]["_source"]
    return {"error": "Sequence number not found"}

@app.get("/high-latency")
def get_high_latency(min_latency: float = Query(500, description="Minimum latency threshold")):
    """Get all messages with latency greater than threshold"""
    query = {
        "query": {
            "range": {"latency": {"gt": min_latency}}
        },
        "size": 100  # Limit to 100 results
    }
    result = es.search(index="smpp-latency", body=query)
    return [hit["_source"] for hit in result["hits"]["hits"]]

@app.get("/errors")
def get_failed_messages():
    """Retrieve messages with non-zero command_status (errors)"""
    query = {"query": {"range": {"command_status": {"gt": 0}}}, "size": 100}
    result = es.search(index="smpp-errors", body=query)
    return [hit["_source"] for hit in result["hits"]["hits"]]

@app.get("/packet/{packet_number}")
def get_packet(packet_number: int):
    """Retrieve raw SMPP packet by packet number"""
    query = {"query": {"match": {"packet_number": packet_number}}}
    result = es.search(index="smpp-packets", body=query)
    if result["hits"]["total"]["value"] > 0:
        return result["hits"]["hits"][0]["_source"]
    return {"error": "Packet not found"}

