import redis
import json
import os

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

QUEUE_NAME = "incident_queue"
DEDUP_KEY_PREFIX = "incident_lock:"


def push_signal(signal):
    """
    Push signal to queue with debouncing
    """
    component = signal["component"]

    lock_key = f"{DEDUP_KEY_PREFIX}{component}"

    # Debounce: skip if lock exists
    if r.get(lock_key):
        print(f"[DEBOUNCE] Skipping duplicate signal for {component}")
        return False

    # Set lock for 30 seconds
    r.set(lock_key, "1", ex=30)

    r.lpush(QUEUE_NAME, json.dumps(signal))
    return True


def pop_signal():
    data = r.rpop(QUEUE_NAME)
    if data:
        return json.loads(data)
    return None
