"""Verifier check: every number in a card's front or back appears in the text of the lesson the card names.

Usage (from the checkout root, after extracting lesson text to /tmp/e2-v/d/L0n.txt):
    .venv/bin/python -I ledgers/E2/scripts/E2-d-r1/check_cards_numbers.py
Prints the missing (card, lesson, number) triples; prints 0 missing on the pinned checkout.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CARDS = json.loads((ROOT / "course/modules/E/E2/cards.json").read_text(encoding="utf-8"))
TEXT = {
    lesson: (Path("/tmp/e2-v/d") / f"{lesson}.txt").read_text(encoding="utf-8").replace(",", "")
    for lesson in sorted({c["lesson"] for c in CARDS})
}
missing = []
for card in CARDS:
    for number in set(re.findall(r"(?<![A-Za-z_])\d[\d,]*\.?\d*", card["front"] + " " + card["back"])):
        token = number.replace(",", "").rstrip(".")
        if len(token) >= 2 and token not in TEXT[card["lesson"]]:
            missing.append((card["id"], card["lesson"], token))
print(f"cards {len(CARDS)}, numbers missing from their lesson: {len(missing)}")
for item in missing:
    print(*item)
