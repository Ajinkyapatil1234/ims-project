from sqlalchemy import Column, Integer, String, DateTime
from app.db import Base
from datetime import datetime

class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)
    component = Column(String, nullable=False)
    status = Column(String, default="OPEN")  # OPEN → INVESTIGATING → RESOLVED → CLOSED
    severity = Column(String)
    description = Column(String)

    created = Column(DateTime, default=datetime.utcnow)
    resolved = Column(DateTime, nullable=True)

    rca = Column(String, nullable=True)

    mttr = Column(Integer, nullable=True)  # in seconds
