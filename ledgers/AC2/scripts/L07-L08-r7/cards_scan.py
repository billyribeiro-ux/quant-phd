"""Scan AC2 cards: count, id sequence, duplicate fronts/backs, L07 and L08 cards, banned strings."""
import json, re, sys, collections
path = sys.argv[1]
cards = json.load(open(path, encoding="utf-8"))
print("count", len(cards))
ids = [c["id"] for c in cards]
print("ids unique", len(set(ids)) == len(ids), "first", ids[0], "last", ids[-1])
print("sequence c001-c140", ids == [f"AC2-c{i:03d}" for i in range(1, 141)])
fr = collections.Counter(c["front"].strip().lower() for c in cards)
bk = collections.Counter(c["back"].strip().lower() for c in cards)
print("duplicate fronts", [k for k, v in fr.items() if v > 1])
print("duplicate backs", [k for k, v in bk.items() if v > 1])
for c in cards:
    if c["lesson"] in ("L07", "L08"):
        print(c["id"], c["lesson"], c.get("grade"), "|", c["front"][:90], "|", c["back"][:100])
