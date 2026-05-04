from sqlalchemy.orm import Session
from datetime import datetime
from app.models.incident import Incident

def create_incident(db: Session, component: str, severity: str):
    incident = Incident(
        component=component,
        severity=severity,
        status="OPEN"
    )
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident


def resolve_incident(db: Session, incident_id: int, rca: str):
    incident = db.query(Incident).filter(Incident.id == incident_id).first()

    if not incident:
        return None

    if not rca:
        raise Exception("RCA is mandatory to close incident")

    incident.status = "CLOSED"
    incident.resolved = datetime.utcnow()
    incident.rca = rca

    # MTTR calculation
    incident.mttr = str(incident.resolved - incident.created)

    db.commit()
    return incident


def ingest_signal(db: Session, component: str, severity: str):
    # SIMPLE DEBOUNCING:
    existing = db.query(Incident).filter(
        Incident.component == component,
        Incident.status == "OPEN"
    ).first()

    if existing:
        return existing

    return create_incident(db, component, severity)
