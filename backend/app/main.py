# app/main.py

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime

from app.db import SessionLocal, engine, Base
from app.models import Incident
from app.utils.queue import push_signal


# Create DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI()


# Allow frontend (localhost:5500)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------------------
# Health Check
# ---------------------------
@app.get("/")
def root():
    return {"message": "IMS Backend Running"}


# ---------------------------
# Get all incidents
# ---------------------------
@app.get("/incidents")
def get_incidents(db: Session = Depends(get_db)):
    incidents = db.query(Incident).order_by(Incident.id.desc()).all()
    return incidents


# ---------------------------
# Create incident (manual)
# ---------------------------
@app.post("/incidents")
def create_incident(data: dict, db: Session = Depends(get_db)):
    try:
        component = data.get("component")
        severity = data.get("severity")
        description = data.get("description")

        if not component or not severity or not description:
            return {"error": "component, severity, description required"}

        incident = Incident(
            component=component,
            severity=severity,
            description=description,
            status="OPEN",
            created=datetime.utcnow(),
        )

        db.add(incident)
        db.commit()
        db.refresh(incident)

        return incident

    except Exception as e:
        return {"error": str(e)}


# ---------------------------
# Resolve incident
# ---------------------------
@app.post("/resolve/{incident_id}")
def resolve_incident(incident_id: int, data: dict, db: Session = Depends(get_db)):
    try:
        incident = db.query(Incident).filter(Incident.id == incident_id).first()

        if not incident:
            return {"error": "Incident not found"}

        if incident.status == "RESOLVED":
            return {"message": "Already resolved"}

        incident.status = "RESOLVED"
        incident.resolved = datetime.utcnow()
        incident.rca = data.get("rca", "")

        db.commit()

        return {"message": "Incident resolved"}

    except Exception as e:
        return {"error": str(e)}


# ---------------------------
# Signal ingestion (Debounce)
# ---------------------------
@app.post("/signal")
def ingest_signal(data: dict):
    """
    Example:
    {
      "component": "API_SERVER",
      "severity": "P1",
      "description": "CPU High"
    }
    """

    try:
        required = ["component", "severity", "description"]

        for field in required:
            if field not in data:
                return {"error": f"{field} is required"}

        pushed = push_signal(data)

        if not pushed:
            return {"message": "Duplicate signal ignored (debounced)"}

        return {"message": "Signal accepted"}

    except Exception as e:
        return {"error": str(e)}
