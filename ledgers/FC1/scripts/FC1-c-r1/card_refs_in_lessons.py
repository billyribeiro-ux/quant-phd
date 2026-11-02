"""For each card, checks that every cited block label (Definition x.y, Proposition x.y, Remark, Example, Problem,
Corollary, Assumption, Section, Lab part, misconception n) occurs in the card's own lesson page text.

Usage: python -I card_refs_in_lessons.py <module dir>
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

module = Path(sys.argv[1])
cards = json.loads((module / "cards.json").read_text(encoding="utf-8"))
texts: dict[str, str] = {}
for lesson in ("L01", "L02", "L03", "L04", "L05"):
    raw = (module / f"{lesson}.html").read_text(encoding="utf-8")
    texts[lesson] = html.unescape(re.sub(r"<[^>]+>", " ", raw))
pattern = re.compile(
    r"\b(Definition|Proposition|Remark|Example|Problem|Corollary|Assumption|Section|misconception|Lab \d, Part)\s?([A-Z]?\d[\d.]*(?:\([ivx]+\))?|[A-Z]\d|[A-Z]\b|[A-D]\b)?"
)
bad = 0
checked = 0
for card in cards:
    text = texts[card["lesson"]]
    for match in pattern.finditer(card["front"] + " " + card["back"]):
        label = match.group(0).strip()
        checked += 1
        if label not in text and not any(label.startswith(p) for p in ()):
            other = [l for l, t in texts.items() if label in t]
            bad += 1
            print(f"{card['id']} ({card['lesson']}): '{label}' not in own lesson; found in {other or 'no lesson'}")
print(f"refs checked={checked} unresolved={bad}")
