from elasticsearch import Elasticsearch
from config import ELASTICSEARCH_HOST, INDEX_NAME

# Initialize Elasticsearch Client
es = Elasticsearch([ELASTICSEARCH_HOST])

def store_in_elasticsearch(data):
    """Stores parsed SMPP data in Elasticsearch."""
    es.index(index=INDEX_NAME, document=data)
    print(f"📦 Stored in ES: {data}")

def update_command_status(sequence_number, command_status, response_time_ms, message_type):
    """Updates command_status and response time in Elasticsearch."""
    query = {
        "script": {
            "source": """
                ctx._source.command_status = params.command_status;
                ctx._source.response_time_ms = params.response_time_ms;
                ctx._source.response_time_ms = params.response_time_ms - ctx._source.submit_time_ms;
            """,
            "lang": "painless",
            "params": {
                "command_status": command_status,
                "response_time_ms": response_time_ms
            }
        },
        "query": {
            "bool": {
                "must": [
                    {"match": {"sequence_number": sequence_number}},
                    {"match": {"message_type": message_type}}
                ]
            }
        }
    }
    es.update_by_query(index=INDEX_NAME, body=query)
    print(f"✅ Updated {message_type}: sequence_number={sequence_number}, command_status={command_status}, response_time_ms calculated")
