"""Dump M5 cards for lessons L01-L04 and check duplicates across all M5 cards (read-only)."""
import json
import sys
from collections import Counter

path = sys.argv[1]
lessons = set(sys.argv[2].split(","))
cards = json.load(open(path, encoding="utf-8"))
print("total cards:", len(cards))
ids = Counter(c["id"] for c in cards)
dups = [i for i, n in ids.items() if n > 1]
print("duplicate ids:", dups)
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts:", [f[:60] for f, n in fronts.items() if n > 1])
backs = Counter(c["back"].strip().lower() for c in cards)
print("duplicate backs:", [f[:60] for f, n in backs.items() if n > 1])
print("keys:", sorted({k for c in cards for k in c}))
print("grades:", Counter(c.get("grade") for c in cards))
for c in cards:
    if c["lesson"] in lessons:
        print(json.dumps(c, ensure_ascii=False))
