"""Dump the cards of lessons L05-L08 of E3 with ids, grades, cites, basis, and counts."""
import json
import sys
from collections import Counter

path = sys.argv[1]
lessons = set(sys.argv[2].split(",")) if len(sys.argv) > 2 else {"L05", "L06", "L07", "L08"}
cards = json.load(open(path, encoding="utf-8"))
print("total cards", len(cards))
print("keys per card", Counter(tuple(sorted(c.keys())) for c in cards))
print("lessons", Counter(c["lesson"] for c in cards))
ids = Counter(c["id"] for c in cards)
print("duplicate ids", [k for k, v in ids.items() if v > 1])
sel = [c for c in cards if c["lesson"] in lessons]
print("selected", len(sel), Counter(c["lesson"] for c in sel))
for c in sel:
    print(json.dumps(c, ensure_ascii=False))
