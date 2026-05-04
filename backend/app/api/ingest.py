from fastapi import APIRouter
import redis
import json
from datetime import datetime

router = APIRouter()

r = redis.Redis(host='redis', port=6379, decode_responses=True)

@router.post("/ingest")
def ingest_signal(signal: dict):
    signal["timestamp"] = str(datetime.utcnow())

    # push to queue
    r.lpush("signal_queue", json.dumps(signal))

    return {"message": "Signal received"}
