import json
from datetime import datetime

def load_json(file):
    with open(file, 'r') as f:
        return json.load(f)

def save_json(file, data):
    with open(file, 'w') as f:
        json.dump(data, f, indent=4)

history = load_json("data/history.json")
today = "2024-10-05"

print("Before reset:")
print(f"Today's date: {today}")
for o in history:
    print(f"Order {o['id']}: {o['date_time']}")

# Reset logic
history = [
    o for o in history
    if not (o.get("date_time") and o["date_time"].startswith(today))
]

save_json("data/history.json", history)

print("\nAfter reset:")
for o in history:
    print(f"Order {o['id']}: {o['date_time']}")
