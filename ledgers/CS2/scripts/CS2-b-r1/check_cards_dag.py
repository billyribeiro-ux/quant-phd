"""Verifier round 1 (CS2-b): full duplicate scan of CS2 cards, card-lesson coverage, and CS2 prerequisite closure
from curriculum/curriculum.json. Run: <checkout>/.venv/bin/python -I <checkout>/ledgers/CS2/scripts/CS2-b-r1/check_cards_dag.py
"""
import json
import re
from collections import Counter

cards = json.load(open("course/modules/CS/CS2/cards.json", encoding="utf8"))
ids = Counter(c["id"] for c in cards)
fronts = Counter(c["front"].strip().lower() for c in cards)
print("cards", len(cards), "duplicate ids", [k for k, v in ids.items() if v > 1], "duplicate fronts", [k for k, v in fronts.items() if v > 1])
lessons = Counter(c["lesson"] for c in cards)
print("cards per lesson", dict(sorted(lessons.items())))
for c in cards:
    if c["lesson"] in ("L05", "L06", "L07", "L08"):
        pass
# near-duplicate fronts (same first 6 words)
heads = Counter(" ".join(c["front"].lower().split()[:6]) for c in cards)
print("near-duplicate front heads", [k for k, v in heads.items() if v > 1])

cur = json.load(open("curriculum/curriculum.json", encoding="utf8"))
mods = {}
def walk(o):
    if isinstance(o, dict):
        if "id" in o and "prereqs" in o and "concepts" in o or ("id" in o and o.get("id") == "CS2"):
            mods[o["id"]] = o
        for v in o.values():
            walk(v)
    elif isinstance(o, list):
        for v in o:
            walk(v)
walk(cur)
cs2 = mods.get("CS2")
print("CS2 prereqs:", cs2.get("prereqs") if cs2 else "missing")
def closure(m, seen=None):
    seen = set() if seen is None else seen
    for p in mods.get(m, {}).get("prereqs", []):
        if p not in seen:
            seen.add(p)
            closure(p, seen)
    return seen
print("CS2 closure:", sorted(closure("CS2")))
