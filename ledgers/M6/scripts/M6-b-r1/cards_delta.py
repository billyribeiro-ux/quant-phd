"""Per-id compare of course/modules/M/M6/cards.json between two JSON files (M6-b round 1).

Usage: python -I cards_delta.py <base.json> <head.json>
Prints changed, added and removed ids with their lesson, the in-slice (L05-L08) counts,
and any duplicate ids or duplicate fronts in either file.
"""
import json
import sys
from collections import Counter

base_path, head_path = sys.argv[1], sys.argv[2]
base = json.load(open(base_path, encoding="utf-8"))
head = json.load(open(head_path, encoding="utf-8"))
SLICE = {"L05", "L06", "L07", "L08"}


def index(cards):
    return {c["id"]: c for c in cards}


bi, hi = index(base), index(head)
print("base cards", len(base), "head cards", len(head))
for label, cards in (("base", base), ("head", head)):
    ids = Counter(c["id"] for c in cards)
    fronts = Counter(c["front"] for c in cards)
    print(label, "duplicate ids", [i for i, n in ids.items() if n > 1], "duplicate fronts", [f for f, n in fronts.items() if n > 1])
    print(label, "in-slice L05-L08 cards", sum(1 for c in cards if c["lesson"] in SLICE))
changed = sorted(i for i in bi if i in hi and bi[i] != hi[i])
added = sorted(i for i in hi if i not in bi)
removed = sorted(i for i in bi if i not in hi)
print("changed", [(i, hi[i]["lesson"]) for i in changed])
print("added", [(i, hi[i]["lesson"]) for i in added])
print("removed", [(i, bi[i]["lesson"]) for i in removed])
print("in-slice changed", [i for i in changed if hi[i]["lesson"] in SLICE])
print("in-slice added", [i for i in added if hi[i]["lesson"] in SLICE])
print("in-slice removed", [i for i in removed if bi[i]["lesson"] in SLICE])
