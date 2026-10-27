"""Round-3 verifier: card inventory, id uniqueness, exact duplicates and near-duplicates across all AC2 cards.

Usage: .venv/bin/python -I ledgers/AC2/scripts/L03-L04-r3/cards_scan.py <checkout>
"""

from __future__ import annotations

import difflib
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/AC/AC2/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)))
print("ids c001..c138 complete:", sorted(ids) == [f"AC2-c{n:03d}" for n in range(1, 139)])
print("per lesson:", dict(sorted(Counter(c["lesson"] for c in cards).items())))
print("L03 ids:", [c["id"][-4:] for c in cards if c["lesson"] == "L03"])
print("L04 ids:", [c["id"][-4:] for c in cards if c["lesson"] == "L04"])
fronts = Counter(c["front"].strip().lower() for c in cards)
backs = Counter(c["back"].strip().lower() for c in cards)
print("exact duplicate fronts:", [f for f, n in fronts.items() if n > 1])
print("exact duplicate backs:", [b for b, n in backs.items() if n > 1])
norm = lambda s: re.sub(r"[^a-z0-9 ]", "", s.lower())
near = []
for i, a in enumerate(cards):
    for b in cards[i + 1 :]:
        ra = difflib.SequenceMatcher(None, norm(a["front"]), norm(b["front"])).ratio()
        if ra >= 0.75:
            near.append((round(ra, 2), a["id"], b["id"], a["front"][:70], b["front"][:70]))
for row in sorted(near, reverse=True):
    print("near-dup front", row)
for c in cards:
    if "about" in c["back"].lower() or "about" in c["front"].lower():
        print("'about' in", c["id"], "|", c["back"][:140])
