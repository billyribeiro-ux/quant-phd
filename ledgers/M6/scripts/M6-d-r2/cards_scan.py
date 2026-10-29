"""Scan M6 cards.json: counts, grades, duplicates by text similarity, and missing bases."""
import difflib
import json
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
print("cards:", len(cards), "ids unique:", len({c["id"] for c in cards}) == len(cards))
print("grades:", Counter(c.get("grade", "<none>") for c in cards))
print("lessons:", sorted(Counter(c["lesson"] for c in cards).items()))
for c in cards:
    g = c.get("grade")
    if g is None:
        print("NO GRADE:", c["id"], c["lesson"], "|", c["front"][:70])
    elif g != "T" and "basis" not in c:
        print("NO BASIS:", c["id"], g)
    elif g == "T" and "basis" in c:
        print("T WITH BASIS:", c["id"])
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        r = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if r > 0.6 or rb > 0.6:
            print("NEAR-DUP", a["id"], b["id"], a["lesson"], b["lesson"], round(r, 2), round(rb, 2))
