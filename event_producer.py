import json
import time
import random
from datetime import datetime

events = [
    {"service": "auth", "level": "info", "msg": "User logged in"},
    {"service": "payments", "level": "error", "msg": "Payment failed"},
    {"service": "orders", "level": "info", "msg": "Order created"},
    {"service": "inventory", "level": "warning", "msg": "Low stock"},
]

while True:
    event = random.choice(events)
    event["timestamp"] = datetime.utcnow().isoformat()

    with open("event_stream.jsonl", "a") as f:
        f.write(json.dumps(event) + "\n")

    print("Produced:", event)
    time.sleep(2)
