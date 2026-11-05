"""Compare SC1 cards.json between two JSON files; print ids changed, added, removed, grouped by lesson.

Usage: python -I cards_delta.py <old.json> <new.json>
"""
import json
import sys
from collections import Counter

old = json.load(open(sys.argv[1], encoding="utf-8"))
new = json.load(open(sys.argv[2], encoding="utf-8"))
ol = old if isinstance(old, list) else old.get("cards", old)
nl = new if isinstance(new, list) else new.get("cards", new)
od = {c["id"]: c for c in ol}
nd = {c["id"]: c for c in nl}
print("counts old/new:", len(od), len(nd))
print("removed:", sorted(set(od) - set(nd)))
print("added:", sorted(set(nd) - set(od)))
changed = sorted(k for k in set(od) & set(nd) if od[k] != nd[k])
print("changed:", len(changed))
print("changed by lesson:", dict(Counter(nd[k]["lesson"] for k in changed)))
for k in changed:
    if nd[k]["lesson"] in ("L07", "L08"):
        print("CHANGED", k, nd[k]["lesson"], [f for f in nd[k] if od[k].get(f) != nd[k].get(f)])
print("lesson counts new:", dict(Counter(c["lesson"] for c in nl)))
