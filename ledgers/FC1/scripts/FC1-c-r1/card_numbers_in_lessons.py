"""For each card in cards.json, lists numeric tokens that do not occur in the card's lesson page text.

Text of the lesson page (tags stripped, entities unescaped, thousands separators removed) is searched for each token
with thousands separators removed. Usage: python -I card_numbers_in_lessons.py <module dir>
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
    body = re.sub(r"<[^>]+>", " ", raw)
    body = html.unescape(body)
    texts[lesson] = re.sub(r"(?<=\d),(?=\d{3})", "", body)
token = re.compile(r"(?<![\w.])\d+(?:\.\d+)?")
misses = 0
for card in cards:
    text = texts[card["lesson"]]
    for number in sorted(set(token.findall(card["front"] + " " + card["back"]))):
        cleaned = number
        if cleaned not in text:
            misses += 1
            print(f"{card['id']} ({card['lesson']}): '{number}' not in {card['lesson']}.html | {card['front'][:70]}")
print(f"cards={len(cards)} missing_number_tokens={misses}")
