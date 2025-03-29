from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from kafka import KafkaProducer
from config.kafka_config import KAFKA_BROKER

router = APIRouter()

@router.get("/health")
def health_check():
    """
    Basic health check to see if API is running.
    """
    return {"status": "API is running"}

@router.get("/db-health")
def db_health_check(db: Session = Depends(get_db)):
    """
    Check if the database is accessible.
    """
    try:
        db.execute("SELECT 1")
        return {"status": "Database is connected"}
    except Exception as e:
        return {"status": "Database connection failed", "error": str(e)}

@router.get("/kafka-health")
def kafka_health_check():
    """
    Check if Kafka is accessible.
    """
    try:
        producer = KafkaProducer(bootstrap_servers=KAFKA_BROKER)
        producer.close()
        return {"status": "Kafka is reachable"}
    except Exception as e:
        return {"status": "Kafka connection failed", "error": str(e)}
