"""Verifier scan of SC1 retrieval cards (round 2, slice b): unique ids, duplicate fronts, coverage of L04-L06.

Run as: python -I -W error ledgers/SC1/scripts/SC1-b-r2/cards_scan.py   (from the checkout root)
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/SC/SC1/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
fronts = Counter(c["front"].strip().lower() for c in cards)
print(f"cards: {len(cards)}; unique ids: {len(set(ids))}")
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
slice_b = [c for c in cards if c["lesson"] in ("L04", "L05", "L06")]
print(f"L04-L06 cards: {len(slice_b)}; first {slice_b[0]['id']}; last {slice_b[-1]['id']}")
print("per lesson:", dict(Counter(c["lesson"] for c in slice_b)))
for c in slice_b:
    if "quadrature error" in c["back"] or "quadrature error" in c["front"]:
        print("quadrature-error wording:", c["id"])
