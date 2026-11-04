"""Dump cards.json grouped by lesson, one card per block, for reading in full."""
import json
import sys
from collections import Counter

data = json.load(open(sys.argv[1], encoding="utf-8"))
cards = data if isinstance(data, list) else data.get("cards", data)
print("TOTAL", len(cards), "keys", sorted(set(k for c in cards for k in c)))
print("PER-LESSON", sorted(Counter(c["lesson"] for c in cards).items()))
want = sys.argv[2] if len(sys.argv) > 2 else None
for c in cards:
    if want and c["lesson"] != want:
        continue
    print(f"{c['id']} {c['lesson']} grade={c.get('grade')} basis={c.get('basis')}")
    print(f"  F: {c['front']}")
    print(f"  B: {c['back']}")
