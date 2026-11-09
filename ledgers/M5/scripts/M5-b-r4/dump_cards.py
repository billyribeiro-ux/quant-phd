"""Dump the cards of lessons L05-L07 of M5 (slice b) and check ids, grades and basis fields."""
import json
import sys
from collections import Counter

path = "course/modules/M/M5/cards.json"
cards = json.load(open(path, encoding="utf-8"))
print("total cards", len(cards))
ids = Counter(c["id"] for c in cards)
dups = [k for k, v in ids.items() if v > 1]
print("duplicate ids", dups)
keys = Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets", keys)
slice_cards = [c for c in cards if c["lesson"] in ("L05", "L06", "L07")]
print("slice cards", len(slice_cards), Counter(c["lesson"] for c in slice_cards))
for c in slice_cards:
    print(f"{c['id']} | {c['lesson']} | grade={c.get('grade')} | basis={c.get('basis')} | cite={c.get('cite')}")
    print(f"   F: {c['front']}")
    print(f"   B: {c['back']}")
