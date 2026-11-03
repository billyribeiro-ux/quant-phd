"""Structural scan of E3 cards for L01 to L04 (verifier E3 slice f, round 2).

Prints the card count per lesson, exact duplicate fronts, backs and ids over the whole file, near-duplicate pairs
(difflib ratio above 0.6), grade and basis combinations, symbol hits against notation/notation.json, and any
registry key cited by a slice card. Run with: python3 -I ledgers/E3/scripts/E3-f-r2/scan_cards.py
"""

from __future__ import annotations

import difflib
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/E/E3/cards.json").read_text(encoding="utf-8"))
slice_cards = [c for c in cards if c["lesson"] in {"L01", "L02", "L03", "L04"}]
per_lesson = dict(Counter(c["lesson"] for c in slice_cards))
print(f"cards total {len(cards)}; slice cards {len(slice_cards)}; per lesson {per_lesson}")
for label, key in (("fronts", "front"), ("backs", "back"), ("ids", "id")):
    dups = [k for k, n in Counter(c[key] for c in cards).items() if n > 1]
    print(f"exact duplicate {label} over the whole file: {dups}")
pairs = []
for i, a in enumerate(slice_cards):
    for b in slice_cards[i + 1 :]:
        ratio = difflib.SequenceMatcher(None, a["front"] + " " + a["back"], b["front"] + " " + b["back"]).ratio()
        if ratio > 0.6:
            pairs.append((round(ratio, 2), a["id"], b["id"]))
print(f"near-duplicate pairs in slice (ratio > 0.6): {sorted(pairs, reverse=True)}")
combos = Counter((c.get("grade"), "basis" in c, "cite" in c) for c in slice_cards)
print(f"grade/basis/cite combinations: {dict(combos)}")
no_basis = [c["id"] for c in slice_cards if c.get("grade") == "C" and not str(c.get("basis", "")).strip()]
t_basis = [c["id"] for c in slice_cards if c.get("grade") == "T" and "basis" in c]
print(f"grade C without basis: {no_basis}; grade T carrying a basis: {t_basis}")
symbols = re.compile(r"(?<![A-Za-z])(T|N|S|m|mu|sigma|Phi|R\^|R_f|Q|gamma_3|gamma_4)(?![A-Za-z])")
hits = {c["id"]: symbols.findall(c["front"] + " " + c["back"]) for c in slice_cards}
print("symbol hits (registered T, Phi, gamma_3, gamma_4, R^, R_f, Q; local S, m, mu, sigma, N):")
print({k: v for k, v in hits.items() if v})
cited = [c["id"] for c in slice_cards if c.get("cite")]
print(f"slice cards citing registry keys: {cited}")
