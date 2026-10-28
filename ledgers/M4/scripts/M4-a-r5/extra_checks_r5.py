"""Round-5 extra checks for M4-a: Python rounding of 148.5, card dump and duplicate scan.
Run: python -I extra_checks_r5.py <checkout>"""
import collections
import json
import sys

root = sys.argv[1]
print("round(148.5) =", round(148.5), "| math.ceil(148.5) =", __import__("math").ceil(148.5))
print("round(2.5) =", round(2.5), "| round(3.5) =", round(3.5))
cards = json.load(open(root + "/course/modules/M/M4/cards.json", encoding="utf-8"))
print("cards total", len(cards))
ids = collections.Counter(c["id"] for c in cards)
fronts = collections.Counter(c["front"].strip().lower() for c in cards)
print("duplicate ids", [i for i, n in ids.items() if n > 1])
print("duplicate fronts", [f for f, n in fronts.items() if n > 1])
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03", "L04") and c["id"] in ("M4-c007", "M4-c036", "M4-c039", "M4-c040", "M4-c173"):
        print(c["id"], "|", c["back"])
