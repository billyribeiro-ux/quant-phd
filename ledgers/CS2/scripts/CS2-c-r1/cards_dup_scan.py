"""Scan CS2 cards.json for near-duplicate fronts and backs (CS2 slice c round 1)."""
import difflib
import json
import re
import sys

path = sys.argv[1]
cards = json.load(open(path, encoding="utf-8"))


def norm(s):
    return re.sub(r"[^a-z0-9 ]", " ", s.lower()).split()


pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rf = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        rb = difflib.SequenceMatcher(None, norm(a["back"]), norm(b["back"])).ratio()
        if rf >= 0.55 or rb >= 0.55:
            pairs.append((round(max(rf, rb), 3), a["id"], a["lesson"], b["id"], b["lesson"], round(rf, 2), round(rb, 2)))
pairs.sort(reverse=True)
for p in pairs[:60]:
    print(p)
print("pairs>=0.55:", len(pairs))
