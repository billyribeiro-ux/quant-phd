"""Round-7 verifier script: every number written on a card's front or back must occur in that card's lesson text
(or in its expected lab block). Numbers that are arithmetic on printed values are reported for manual review.

Usage: python card_numbers_r7.py <checkout-root>
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
tdir = root / "ledgers/CS2/scripts/CS2-d-r7/text"
cards = json.loads((root / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
lesson_text: dict[str, str] = {}
for page in tdir.glob("L??.txt"):
    lesson_text[page.stem] = page.read_text(encoding="utf-8") + (tdir / f"{page.stem}.expected.txt").read_text(encoding="utf-8")
num = re.compile(r"(?<![\w.])\d+(?:\.\d+)?(?:e-?\d+)?(?![\w])")
absent = []
for card in cards:
    text = card["front"] + " " + card["back"]
    for token in sorted(set(num.findall(text))):
        if token in lesson_text[card["lesson"]]:
            continue
        absent.append((card["id"], card["lesson"], token))
for item in absent:
    print("NOT IN LESSON OR EXPECTED BLOCK", item)
print("numbers not found verbatim in own lesson:", len(absent))
