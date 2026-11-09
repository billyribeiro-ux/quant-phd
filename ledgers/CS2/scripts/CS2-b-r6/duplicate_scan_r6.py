"""Verifier round 6: near-duplicate scan of the CS2 cards (fronts and backs), slice pairs flagged."""
import difflib
import itertools
import json
import sys

cards = json.load(open(sys.argv[1], encoding="utf-8"))
SLICE = ("L05", "L06", "L07", "L08")
hits = []
for a, b in itertools.combinations(cards, 2):
    if a["lesson"] not in SLICE and b["lesson"] not in SLICE:
        continue
    rf = difflib.SequenceMatcher(None, a["front"].lower(), b["front"].lower()).ratio()
    rb = difflib.SequenceMatcher(None, a["back"].lower(), b["back"].lower()).ratio()
    if rf > 0.6 and rb > 0.6:
        hits.append((a["id"], b["id"], round(rf, 2), round(rb, 2)))
print("slice pairs with front ratio > 0.6 and back ratio > 0.6:", hits)
