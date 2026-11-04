"""Card checks for SC1 L07 and L08 (round 5): duplicate fronts over the whole deck, ids, and card numbers
that must appear in the card's own lesson text. Run from the checkout root:
python -I -W error ledgers/SC1/scripts/SC1-c-r5/cards_check_r5.py
"""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
cards = json.loads((ROOT / "course/modules/SC/SC1/cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)))
fronts = Counter(c["front"] for c in cards)
print("duplicate fronts", [f for f, n in fronts.items() if n > 1])
print("ids not SC1-cNNN", [i for i in ids if not re.fullmatch(r"SC1-c\d{3}", i)])
lesson_text: dict[str, str] = {}
for lesson in ("L07", "L08"):
    raw = (ROOT / f"course/modules/SC/SC1/{lesson}.html").read_text(encoding="utf-8")
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    lesson_text[lesson] = re.sub(r"\s+", " ", text)
num = re.compile(r"\d+(?:\.\d+)?")
for c in cards:
    if c["lesson"] not in lesson_text:
        continue
    body = c["back"]
    missing = []
    for tok in num.findall(body):
        if len(tok) < 2 or tok in ("10", "12", "16", "64", "256", "1000"):
            continue
        if tok not in lesson_text[c["lesson"]]:
            missing.append(tok)
    if missing:
        print(c["id"], c["lesson"], "numbers not in lesson text:", missing)
print("L07/L08 number scan done")
