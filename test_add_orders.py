import json
from datetime import datetime, timedelta

# Load current history
with open('data/history.json', 'r') as f:
    history = json.load(f)

# Add today's order
today = datetime.now()
today_str = today.strftime('%Y-%m-%d %H:%M:%S')
history.append({
    "id": "test_today",
    "table": "2",
    "order_items": [{"name": "Poha", "price": 40}],
    "total": 40,
    "user": "test",
    "payment": "UPI",
    "date_time": today_str
})

# Add yesterday's order
yesterday = today - timedelta(days=1)
yesterday_str = yesterday.strftime('%Y-%m-%d %H:%M:%S')
history.append({
    "id": "test_yesterday",
    "table": "3",
    "order_items": [{"name": "Upma", "price": 35}],
    "total": 35,
    "user": "test",
    "payment": "Cash",
    "date_time": yesterday_str
})

# Save
with open('data/history.json', 'w') as f:
    json.dump(history, f, indent=4)

print("Added test orders: one for today, one for yesterday")
