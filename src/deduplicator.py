import json
import os

HISTORY_FILE = 'data/history.json'

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, 'r') as f:
        try:
            return json.load(f)
        except:
            return []

def save_history(history):
    os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def filter_new_items(items):
    history = load_history()
    new_items = []
    for item in items:
        if item['id'] not in history:
            new_items.append(item)
    return new_items

def mark_as_processed(items):
    history = load_history()
    for item in items:
        if item['id'] not in history:
            history.append(item['id'])
    save_history(history)
