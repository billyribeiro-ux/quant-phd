"""Card checks for M3 slice a (L01-L03 cards in course/modules/M/M3/cards.json).

Run from the checkout root:  .venv/bin/python -I ledgers/M3/scripts/M3-a-r1/cards_check.py
Prints: total cards, unique ids, duplicate fronts and backs over the whole unit, the per-lesson counts,
and for each card of L01-L03 whether every number in its back text appears in the lesson page
(course/modules/M/M3/L01.html, L02.html, L03.html, after removing tags). Number matching is textual and
is a presence check only; the card-to-lesson agreement is judged by reading (see the ledger rows).
"""

from __future__ import annotations

import collections
import json
import re
from pathlib import Path

ROOT = Path(".")
cards = json.loads((ROOT / "course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
print(f"cards: {len(cards)}")
ids = [c["id"] for c in cards]
print(f"unique ids: {len(set(ids)) == len(ids)}")


def norm(s: str) -> str:
    return " ".join(s.lower().split())


fronts = collections.Counter(norm(c["front"]) for c in cards)
backs = collections.Counter(norm(c["back"]) for c in cards)
print(f"duplicate fronts: {[k for k, v in fronts.items() if v > 1]}")
print(f"duplicate backs: {[k for k, v in backs.items() if v > 1]}")
per = collections.Counter(c["lesson"] for c in cards)
print(f"per lesson: {dict(sorted(per.items()))}")

lesson_text: dict[str, str] = {}
for lid in ("L01", "L02", "L03"):
    html = (ROOT / f"course/modules/M/M3/{lid}.html").read_text(encoding="utf-8")
    text = re.sub(r"<[^>]+>", " ", html).replace("&lt;", "<").replace("&gt;", ">")
    lesson_text[lid] = " ".join(text.split())

for c in cards:
    if c["lesson"] not in lesson_text:
        continue
    numbers = set(re.findall(r"\d+(?:\.\d+)?", c["back"]))
    missing = sorted(n for n in numbers if n not in lesson_text[c["lesson"]])
    if missing:
        print(f"{c['id']} ({c['lesson']}): numbers not found in lesson text: {missing}")
print("number presence scan done for L01-L03 cards")
