"""Round-4 card scan for M5 slice c (L08-L10 cards): ids unique, grade/basis consistency, near-duplicate pairs."""

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/M/M5/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards total", len(cards), "unique ids", len(set(ids)), "dupe ids", [i for i, n in Counter(ids).items() if n > 1])
slice_cards = [c for c in cards if c["lesson"] in ("L08", "L09", "L10")]
print("slice cards", len(slice_cards), Counter(c["lesson"] for c in slice_cards))
for c in slice_cards:
    g, b = c.get("grade"), c.get("basis")
    if (g is None) != (b is None):
        print("GRADE/BASIS MISMATCH", c["id"], g, b)
    if g not in (None, "T", "C"):
        print("ODD GRADE", c["id"], g)
def toks(c):
    return set(re.findall(r"[a-z]{4,}|\d[\d.]*", (c["front"] + " " + c["back"]).lower()))
pairs = []
for i, a in enumerate(slice_cards):
    for b in slice_cards[i + 1:]:
        ta, tb = toks(a), toks(b)
        j = len(ta & tb) / max(1, len(ta | tb))
        if j >= 0.30:
            pairs.append((round(j, 2), a["id"], b["id"]))
for p in sorted(pairs, reverse=True)[:25]:
    print("NEAR", p)
# cross-check: every card number appears in its lesson text (sample of numbers in back)
