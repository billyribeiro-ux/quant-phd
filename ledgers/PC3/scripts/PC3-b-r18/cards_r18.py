"""PC3-b round 18: card counts per lesson, duplicate ids, and near-duplicate card text in PC3 cards.json.

Usage: python -I ledgers/PC3/scripts/PC3-b-r18/cards_r18.py <repo-root>
"""
import collections
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
print("total PC3 cards", len(cards))
print("by lesson", dict(sorted(collections.Counter(c["lesson"] for c in cards).items())))
ids = [c["id"] for c in cards]
print("duplicate ids", [k for k, v in collections.Counter(ids).items() if v > 1])
print("cards with empty cite-list but cite key present:", sum(1 for c in cards if "cite" in c and c["cite"]))
ls = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print("L04-L06 cards", len(ls), dict(sorted(collections.Counter(c["lesson"] for c in ls).items())))


def words(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))


pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = words(cards[i]["front"]), words(cards[j]["front"])
        if not a or not b:
            continue
        jac = len(a & b) / len(a | b)
        if jac >= 0.45:
            pairs.append((round(jac, 2), cards[i]["id"], cards[j]["id"]))
pairs.sort(reverse=True)
print("front-text Jaccard >= 0.45 pairs:", len(pairs))
for p in pairs[:40]:
    print(" ", p)
for cid in ("PC3-c062", "PC3-c112", "PC3-c123", "PC3-c191", "PC3-c192"):
    c = next(x for x in cards if x["id"] == cid)
    print(cid, c["lesson"], "grade" in c and c["grade"], c.get("basis", ""))
