
import json

def show_security_events(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    security_events = [x for x in data if x.get('type') == 'SECURITY']
    print(f"Found {len(security_events)} SECURITY events.")
    for evt in security_events:
        print(f"[{evt['timestamp']}] {evt['subtype']}: {evt['content']}")

if __name__ == "__main__":
    show_security_events("logs/unified_timeline.json")
