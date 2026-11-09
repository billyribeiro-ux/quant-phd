"""Scan course/modules/M/M2/cards.json for the slice lessons L01-L06: counts, duplicate ids, near-duplicate pairs.

Run: python -I ledgers/M2/scripts/M2-a-r1/cards_scan.py
"""
import itertools
import json
import re
from collections import Counter

PATH = "course/modules/M/M2/cards.json"
SLICE = {"L01", "L02", "L03", "L04", "L05", "L06"}
cards = json.load(open(PATH, encoding="utf-8"))
mine = [c for c in cards if c["lesson"] in SLICE]
print("cards in slice:", len(mine), sorted(Counter(c["lesson"] for c in mine).items()))
print("duplicate ids overall:", [k for k, v in Counter(c["id"] for c in cards).items() if v > 1])
print("ids outside M2 prefix:", [c["id"] for c in cards if not c["id"].startswith("M2-c")])
print("ids out of sequence in slice:", sorted(c["id"] for c in mine if int(c["id"][4:]) > 74))


def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower())) - {"the", "a", "an", "is", "of", "in", "and", "to", "does", "what", "for", "at", "on", "with", "by"}


pairs = []
for x, y in itertools.combinations(mine, 2):
    tx, ty = toks(x["front"] + " " + x["back"]), toks(y["front"] + " " + y["back"])
    j = len(tx & ty) / max(1, len(tx | ty))
    if j >= 0.30:
        pairs.append((round(j, 2), x["id"], y["id"], x["front"][:70], y["front"][:70]))
for p in sorted(pairs, reverse=True)[:15]:
    print(p)
