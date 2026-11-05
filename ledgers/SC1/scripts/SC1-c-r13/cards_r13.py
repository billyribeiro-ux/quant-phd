"""Card checks for SC1 slice c (L07, L08), round 13.

Usage: python -I cards_r13.py <checkout-root>
Prints: card totals, duplicate ids/fronts/backs over the whole file, near-duplicate fronts (ratio > 0.75),
the L07/L08 card list with grade and basis presence, and any numeric token of an L07/L08 card that does not
occur verbatim in its lesson page.
"""
import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/SC/SC1/cards.json").read_text(encoding="utf-8"))
print("total cards", len(cards))
print("duplicate ids", [k for k, v in Counter(c["id"] for c in cards).items() if v > 1])
print("duplicate fronts", [k[:60] for k, v in Counter(c["front"].strip().lower() for c in cards).items() if v > 1])
print("duplicate backs", [k[:60] for k, v in Counter(c["back"].strip().lower() for c in cards).items() if v > 1])
print("lessons", dict(Counter(c["lesson"] for c in cards)))
pairs = []
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        r = difflib.SequenceMatcher(None, cards[i]["front"], cards[j]["front"]).ratio()
        if r > 0.75:
            pairs.append((round(r, 2), cards[i]["id"], cards[j]["id"]))
print("near-duplicate fronts (ratio > 0.75):", sorted(pairs, reverse=True))
pages = {L: (root / f"course/modules/SC/SC1/{L}.html").read_text(encoding="utf-8") for L in ("L07", "L08")}
for c in cards:
    if c["lesson"] not in pages:
        continue
    print(c["id"], c["lesson"], c.get("grade", "-"), "basis" if c.get("basis") else "no-basis")
    txt = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    for tok in sorted(set(re.findall(r"\d+\.\d+|\d{2,}", txt))):
        if tok not in pages[c["lesson"]]:
            print("  NUMBER NOT IN LESSON:", c["id"], tok)
