from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import SMPPTransaction, SMPPLatency, SMPPAlert
from typing import List
from datetime import datetime

router = APIRouter()

@router.get("/transactions/{sequence_number}", response_model=dict)
def get_transaction(sequence_number: int, db: Session = Depends(get_db)):
    """
    Get SMPP transaction details by sequence number.
    """
    transaction = db.query(SMPPTransaction).filter(SMPPTransaction.sequence_number == sequence_number).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return {
        "sequence_number": transaction.sequence_number,
        "source_ip": transaction.source_ip,
        "source_port": transaction.source_port,
        "dest_ip": transaction.dest_ip,
        "dest_port": transaction.dest_port,
        "command_id": transaction.command_id,
        "command_status": transaction.command_status,
        "submit_time": transaction.submit_time,
        "submit_resp_time": transaction.submit_resp_time,
        "latency_ms": transaction.latency_ms
    }

@router.get("/latency", response_model=dict)
def get_latency_stats(db: Session = Depends(get_db)):
    """
    Get latency statistics (min, max, mean).
    """
    latencies = db.query(SMPPLatency.latency_ms).all()
    latencies = [l[0] for l in latencies]

    if not latencies:
        return {"message": "No latency data available"}

    return {
        "min_latency_ms": min(latencies),
        "max_latency_ms": max(latencies),
        "mean_latency_ms": sum(latencies) / len(latencies),
    }

@router.get("/alerts", response_model=List[dict])
def get_alerts(db: Session = Depends(get_db)):
    """
    Get the latest alerts.
    """
    alerts = db.query(SMPPAlert).order_by(SMPPAlert.timestamp.desc()).limit(10).all()
    return [{"timestamp": alert.timestamp, "message": alert.alert_message} for alert in alerts]

@router.get("/transactions", response_model=List[dict])
def get_all_transactions(db: Session = Depends(get_db)):
    """
    Get a list of all SMPP transactions.
    """
    transactions = db.query(SMPPTransaction).limit(100).all()
    return [
        {
            "sequence_number": t.sequence_number,
            "source_ip": t.source_ip,
            "source_port": t.source_port,
            "dest_ip": t.dest_ip,
            "dest_port": t.dest_port,
            "command_id": t.command_id,
            "command_status": t.command_status,
            "submit_time": t.submit_time,
            "submit_resp_time": t.submit_resp_time,
            "latency_ms": t.latency_ms
        }
        for t in transactions
    ]
