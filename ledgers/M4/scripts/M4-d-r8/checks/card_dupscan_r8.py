"""Duplicate scan of cards.json (round 8, slice d): identical fronts, near-identical fronts (difflib ratio >= 0.95),
duplicate ids, and the grade of every card carrying a basis. Usage: python -I .../card_dupscan_r8.py
"""

import collections
import difflib
import json
import pathlib
import re

CARDS = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-M4-d/course/modules/M/M4/cards.json")
cards = json.loads(CARDS.read_text(encoding="utf-8"))


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower())


ids = collections.Counter(c["id"] for c in cards)
print("cards:", len(cards), "duplicate ids:", [k for k, v in ids.items() if v > 1])
fronts = collections.defaultdict(list)
for c in cards:
    fronts[c["front"]].append(c["id"])
print("identical fronts:", {k: v for k, v in fronts.items() if len(v) > 1})
near = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        r = difflib.SequenceMatcher(None, norm(cards[i]["front"]), norm(cards[j]["front"])).ratio()
        if r >= 0.95 and cards[i]["front"] != cards[j]["front"]:
            near.append((round(r, 2), cards[i]["id"], cards[j]["id"]))
print("near-identical fronts (>=0.95, not identical):", sorted(near, reverse=True))
print("grades:", collections.Counter(c["grade"] for c in cards))
for c in cards:
    if "basis" in c or c["grade"] == "C":
        pass
print("C cards:", [c["id"] for c in cards if c["grade"] == "C"])
print("cards with basis:", [c["id"] for c in cards if "basis" in c])
