from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class SMPPTransaction(Base):
    """Stores Submit_SM and Submit_SM_RESP transactions with latency details."""
    __tablename__ = "smpp_transactions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sequence_number = Column(Integer, unique=True, nullable=False, index=True)
    source_ip = Column(String, nullable=False)
    source_port = Column(Integer, nullable=False)
    dest_ip = Column(String, nullable=False)
    dest_port = Column(Integer, nullable=False)
    command_id = Column(String, nullable=False)  # Submit_SM, Submit_SM_RESP, Deliver_SM, etc.
    command_status = Column(Integer, nullable=True)  # Updated when Submit_SM_RESP is received
    submit_time = Column(DateTime, nullable=False, default=datetime.utcnow)
    submit_resp_time = Column(DateTime, nullable=True)
    latency_ms = Column(Float, nullable=True)  # Time difference in milliseconds

    def __repr__(self):
        return f"<SMPPTransaction(seq={self.sequence_number}, status={self.command_status}, latency={self.latency_ms}ms)>"

class SMPPLatency(Base):
    """Stores latency metrics for analysis and monitoring."""
    __tablename__ = "smpp_latency"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sequence_number = Column(Integer, ForeignKey("smpp_transactions.sequence_number"), unique=True, nullable=False)
    latency_ms = Column(Float, nullable=False)
    submit_time = Column(DateTime, nullable=False, default=datetime.utcnow)

    smpp_transaction = relationship("SMPPTransaction", backref="latency")

    def __repr__(self):
        return f"<SMPPLatency(seq={self.sequence_number}, latency={self.latency_ms}ms)>"

class SMPPAlert(Base):
    """Stores high-latency and error alerts."""
    __tablename__ = "smpp_alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    alert_message = Column(String, nullable=False)

    def __repr__(self):
        return f"<SMPPAlert(time={self.timestamp}, message={self.alert_message})>"

