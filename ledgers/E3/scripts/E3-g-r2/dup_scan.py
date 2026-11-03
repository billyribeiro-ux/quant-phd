"""Full duplicate scan of E3 cards.json: exact duplicate fronts/backs and near-duplicates by sequence similarity.

Usage: dup_scan.py <cards.json>
"""
import difflib
import json
import re
import sys
from itertools import combinations

cards = json.load(open(sys.argv[1], encoding="utf-8"))


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower()).strip()


print("cards", len(cards), "distinct ids", len({c["id"] for c in cards}))
print("exact duplicate fronts:", [(a["id"], b["id"]) for a, b in combinations(cards, 2) if norm(a["front"]) == norm(b["front"])])
print("exact duplicate backs:", [(a["id"], b["id"]) for a, b in combinations(cards, 2) if norm(a["back"]) == norm(b["back"])])
pairs = []
for a, b in combinations(cards, 2):
    fr = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
    br = difflib.SequenceMatcher(None, norm(a["back"]), norm(b["back"])).ratio()
    if fr >= 0.6 or br >= 0.6:
        pairs.append((round(max(fr, br), 3), a["id"], a["lesson"], b["id"], b["lesson"], round(fr, 2), round(br, 2)))
pairs.sort(reverse=True)
print("near-duplicate pairs (front or back similarity >= 0.6):", len(pairs))
for p in pairs:
    print(p)
