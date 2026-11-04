"""Full scan of cards.json for duplicate ids, duplicate fronts/backs, and near-duplicate pairs
(difflib ratio on front+back). Read-only. Usage: duplicate_scan.py <cards.json> [threshold]
"""
import difflib
import json
import sys
from collections import Counter

cards = json.load(open(sys.argv[1], encoding="utf-8"))
thr = float(sys.argv[2]) if len(sys.argv) > 2 else 0.6
ids = Counter(c["id"] for c in cards)
print("cards:", len(cards), "distinct ids:", len(ids), "duplicate ids:", [i for i, n in ids.items() if n > 1])
fr = Counter(c["front"] for c in cards)
bk = Counter(c["back"] for c in cards)
print("duplicate fronts:", [f for f, n in fr.items() if n > 1])
print("duplicate backs:", [b for b, n in bk.items() if n > 1])
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a = cards[i]["front"] + " || " + cards[i]["back"]
        b = cards[j]["front"] + " || " + cards[j]["back"]
        r = difflib.SequenceMatcher(None, a, b, autojunk=False).ratio()
        if r >= thr:
            pairs.append((round(r, 3), cards[i]["id"], cards[j]["id"]))
pairs.sort(reverse=True)
print(f"pairs with ratio >= {thr}: {len(pairs)}")
for p in pairs[:25]:
    print("  ", p)
