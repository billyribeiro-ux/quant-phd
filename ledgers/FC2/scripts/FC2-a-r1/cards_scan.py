"""Duplicate and structure scan of course/modules/FC/FC2/cards.json (verifier, round 1).

Run: python -I ledgers/FC2/scripts/FC2-a-r1/cards_scan.py <checkout-root>
Reports duplicate ids, identical fronts or backs, near-duplicate pairs (token Jaccard >= 0.6),
cards whose lesson is not in L01-L08, cards missing a lesson, and graded cards without a basis when
the back names a lab. Also prints the L01-L03 card ids.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/FC/FC2/cards.json").read_text(encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
print("cards:", len(cards), "distinct ids:", len(ids), "duplicate ids:", [i for i, n in ids.items() if n > 1])
print("lessons:", sorted(Counter(c["lesson"] for c in cards).items()))
print("fronts duplicated:", [f for f, n in Counter(c["front"] for c in cards).items() if n > 1])
print("backs duplicated:", [f for f, n in Counter(c["back"] for c in cards).items() if n > 1])


def toks(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))


pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a = toks(cards[i]["front"] + " " + cards[i]["back"])
        b = toks(cards[j]["front"] + " " + cards[j]["back"])
        if not a or not b:
            continue
        jac = len(a & b) / len(a | b)
        if jac >= 0.6:
            pairs.append((round(jac, 2), cards[i]["id"], cards[j]["id"]))
print("near-duplicate pairs (jaccard>=0.6):", sorted(pairs, reverse=True)[:20])
bad_lab = [c["id"] for c in cards if re.search(r"Lab \d|Problem [A-Z]\d|Solution", c["back"] + c["front"]) and "basis" not in c and c.get("grade") not in (None,)]
print("graded cards naming a lab/problem without basis:", bad_lab)
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03"):
        print(c["id"], c["lesson"], c.get("grade", "-"), c.get("basis", "-"))
