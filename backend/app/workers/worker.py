import time
from app.utils.queue import pop_signal
from app.db import SessionLocal
from app.models import Incident
from datetime import datetime


def process_signal(signal):
    db = SessionLocal()

    component = signal["component"]
    severity = signal["severity"]
    description = signal["description"]

    # Check if open incident already exists
    existing = db.query(Incident).filter(
        Incident.component == component,
        Incident.status == "OPEN"
    ).first()

    if existing:
        print(f"[SKIP] Incident already open for {component}")
        db.close()
        return

    incident = Incident(
        component=component,
        severity=severity,
        description=description,
        status="OPEN",
        created=datetime.utcnow()
    )

    db.add(incident)
    db.commit()
    db.close()

    print(f"[CREATED] Incident for {component}")


def run_worker():
    print("Worker started...")

    while True:
        signal = pop_signal()

        if signal:
            process_signal(signal)
        else:
            time.sleep(2)


if __name__ == "__main__":
    run_worker()
