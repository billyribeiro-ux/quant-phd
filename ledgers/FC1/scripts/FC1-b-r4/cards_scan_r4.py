"""Verifier (FC1-b round 4): card-id uniqueness, lesson coverage, near-duplicate fronts across the FC1 deck."""
import difflib
import json
import re
import sys
from collections import Counter

root = sys.argv[1]
cards = json.load(open(f"{root}/course/modules/FC/FC1/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "duplicate ids", [i for i, n in Counter(ids).items() if n > 1])
print("lessons", dict(Counter(c["lesson"] for c in cards)))
for L in ("L04", "L05"):
    print(L, "cards", sum(1 for c in cards if c["lesson"] == L))
for L in ("L04", "L05"):
    page = open(f"{root}/course/modules/FC/FC1/{L}.html", encoding="utf-8").read()
    for c in cards:
        if c["lesson"] != L:
            continue
        for fld in ("front", "back"):
            for num in set(re.findall(r"\d[\d,.]*\d|\d", c[fld])):
                if num.replace(",", "") not in page.replace(",", ""):
                    print("number not in lesson", c["id"], fld, num)
pairs = []
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        r = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
        if r >= 0.6:
            pairs.append((round(r, 2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
for p in sorted(pairs, reverse=True):
    print("similar fronts", p)
