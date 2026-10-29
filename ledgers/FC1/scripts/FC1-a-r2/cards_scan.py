"""Scan course/modules/FC/FC1/cards.json for L01-L03: counts per lesson, duplicates, and the two card texts under review."""
import json, collections, sys
cards = json.load(open(sys.argv[1], encoding="utf-8"))
per = collections.Counter(c["lesson"] for c in cards)
print("per lesson:", dict(per))
print("duplicate fronts:", [k for k, v in collections.Counter(c["front"].strip().lower() for c in cards).items() if v > 1])
print("duplicate ids:", len(cards) - len({c["id"] for c in cards}))
for c in cards:
    if c["id"] in ("FC1-c009", "FC1-c055"):
        print(c["id"], "|", c["back"][:200])
    if "asks above cost" in c["back"]:
        print("overgeneral phrase in", c["id"])
    if c["id"] == "FC1-c009":
        print("c009 carries A3:", "A3" in c["back"])
