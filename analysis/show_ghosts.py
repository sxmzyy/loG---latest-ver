import json

# Load timeline
with open('logs/unified_timeline.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find GHOST events
ghosts = [e for e in data if e.get('type') == 'GHOST']

print(f"Total GHOST events: {len(ghosts)}")
print("\nFirst 5 GHOST events:")
print("=" * 80)

for i, g in enumerate(ghosts[:5], 1):
    print(f"\n{i}. Timestamp: {g['timestamp']}")
    print(f"   Subtype: {g.get('subtype', 'N/A')}")
    print(f"   Content: {g['content'][:150]}...")
