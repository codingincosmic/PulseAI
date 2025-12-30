import json

def get_recent_events(limit=5):
    try:
        with open("event_stream.jsonl", "r") as f:
            lines = f.readlines()
            return [json.loads(l) for l in lines[-limit:]]
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    events = get_recent_events()
    print("Recent events:")
    for e in events:
        print(e)
