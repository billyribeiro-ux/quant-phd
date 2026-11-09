"""Duplicate and atomicity scan of the E1 cards whose lesson is L01-L03 (verifier round 1, slice a).

Prints every pair of cards (among all E1 cards, so cross-lesson duplicates show) whose front+back token
Jaccard similarity is at least 0.35, plus the cards of this slice with their grade and basis fields.
Usage: python -I card_duplicates.py <repo-root>
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/E/E1/cards.json").read_text(encoding="utf-8"))
STOP = {"the", "a", "an", "of", "is", "and", "in", "to", "for", "at", "under", "with", "on", "that", "it", "by", "does"}


def toks(card: dict) -> set[str]:
    words = re.findall(r"[a-z]+", (card["front"] + " " + card["back"]).lower())
    return {w for w in words if w not in STOP and len(w) > 2}


pairs = 0
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        ta, tb = toks(a), toks(b)
        jac = len(ta & tb) / len(ta | tb)
        if jac >= 0.35:
            pairs += 1
            print(f"SIMILAR {jac:.2f}: {a['id']} ({a['lesson']}) vs {b['id']} ({b['lesson']})")
            print(f"   {a['id']} front: {a['front']}")
            print(f"   {b['id']} front: {b['front']}")
print(f"similar pairs (>=0.35): {pairs}")
ids = [c["id"] for c in cards]
print("duplicate ids:", sorted({x for x in ids if ids.count(x) > 1}))
print("slice a cards:", sum(1 for c in cards if c["lesson"] in ("L01", "L02", "L03")))
for c in cards:
    if c["lesson"] in ("L01", "L02", "L03"):
        print(f"{c['id']} {c['lesson']} grade={c.get('grade')} basis={c.get('basis')} cite={c.get('cite')}")
