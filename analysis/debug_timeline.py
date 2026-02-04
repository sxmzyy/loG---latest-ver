
import json
from collections import Counter
from datetime import datetime

def check_timestamps(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if not data:
        return

    # Sort just in case (though script says it sorts)
    # data.sort(key=lambda x: x['timestamp']) 

    print(f"First Event: {data[0]['timestamp']} ({data[0]['type']})")
    print(f"Last Event: {data[-1]['timestamp']} ({data[-1]['type']})")

    years = Counter()
    for item in data:
        try:
            dt = datetime.fromisoformat(item['timestamp'])
            years[dt.year] += 1
        except: pass
    
    print("\nEvents by Year:")
    for yr, count in years.items():
        print(f"{yr}: {count}")

    print("\nGhost Gap Context (Sample):")
    ghosts = [i for i, x in enumerate(data) if x['type'] == 'GHOST']
    for i in ghosts[:5]:
        prev = data[i-1]
        curr = data[i]
        next_evt = data[i+1] if i+1 < len(data) else None
        print(f"GAP at {curr['timestamp']}:")
        print(f"  Prev: {prev['timestamp']} ({prev['type']} - {prev['subtype']})")
        print(f"  Ghost Content: {curr['content']}")
        if next_evt:
            print(f"  Next: {next_evt['timestamp']} ({next_evt['type']} - {next_evt['subtype']})")

if __name__ == "__main__":
    check_timestamps("logs/unified_timeline.json")
