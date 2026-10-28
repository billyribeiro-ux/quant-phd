"""For every M7 card, list the numeric tokens and cited labels of its back and check each one appears in its lesson.

Usage: .venv/bin/python ledgers/M7/scripts/M7-d-r1/card_numbers.py <checkout-root>
Prints one line per card with a token or label missing from its lesson text (tags stripped, MathJax left as text).
"""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/M/M7/cards.json").read_text(encoding="utf-8"))
texts: dict[str, str] = {}
for lesson in sorted({c["lesson"] for c in cards}):
    raw = (root / f"course/modules/M/M7/{lesson}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<script.*?</script>|<style.*?</style>", " ", raw, flags=re.S)
    texts[lesson] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw)))
missing = 0
for card in cards:
    back = card["back"] + " " + card["front"]
    tokens = set(re.findall(r"(?<![\w.])\d+(?:[./]\d+)*(?:%|\.\d+)?", back))
    labels = set(re.findall(r"(?:Definition|Proposition|Theorem|Lemma|Lab|Problem|Corollary|Example) \d+(?:\.\d+)?|Lab \d", back))
    bad = [t for t in sorted(tokens) if t not in texts[card["lesson"]] and t not in ("0", "1", "2", "3")]
    badl = [l for l in sorted(labels) if l not in texts[card["lesson"]]]
    if bad or badl:
        missing += 1
        print(card["id"], card["lesson"], "tokens:", bad, "labels:", badl, "|", card.get("basis", ""))
print("cards with a token or label not in their lesson:", missing, "of", len(cards))
