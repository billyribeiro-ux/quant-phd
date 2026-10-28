"""Count cards, check ids are unique, and list near-duplicate pairs that involve a L06 to L08 card."""

import difflib
import itertools
import json
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "duplicate ids", [i for i, n in Counter(ids).items() if n > 1])
print("per lesson", sorted(Counter(c["lesson"] for c in cards if c["lesson"] in ("L06", "L07", "L08")).items()))
sl = {c["id"] for c in cards if c["lesson"] in ("L06", "L07", "L08")}
pairs = []
for x, y in itertools.combinations(cards, 2):
    if x["id"] in sl or y["id"] in sl:
        a = x["front"] + " || " + x["back"]
        b = y["front"] + " || " + y["back"]
        r = difflib.SequenceMatcher(None, a, b).ratio()
        if r > 0.6:
            pairs.append((round(r, 2), x["id"], y["id"]))
for p in sorted(pairs, reverse=True):
    print("pair", p)
print("pairs above 0.6", len(pairs))
