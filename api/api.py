from fastapi import FastAPI, Query
import psycopg2
from psycopg2.extras import DictCursor
from database.db import get_db_connection

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to SMPP Insights API"}

@app.get("/latency/{sequence_number}")
def get_latency(sequence_number: int):
    """Get latency for a specific sequence number"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM smpp_data WHERE sequence_number = %s", (sequence_number,))
    result = cur.fetchone()
    cur.close()
    conn.close()
    return result if result else {"error": "Sequence number not found"}

@app.get("/high-latency")
def get_high_latency(min_latency: float = Query(500, description="Minimum latency in ms")):
    """Get messages with high latency"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM smpp_data WHERE latency_ms > %s LIMIT 100", (min_latency,))
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result

@app.get("/errors")
def get_failed_messages():
    """Retrieve messages with non-zero command_status (errors)"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM smpp_data WHERE command_status > 0 LIMIT 100")
    result = cur.fetchall()
    cur.close()
    conn.close()
    return result
