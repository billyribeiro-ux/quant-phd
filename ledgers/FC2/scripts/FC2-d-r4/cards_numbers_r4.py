"""For each FC2 card, list numeric tokens in its front and back that do not occur in the card's lesson text.

Usage: python -I cards_numbers_r4.py <cards.json> <text_dir>
"""

import json
import re
import sys
from pathlib import Path

cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
text_dir = Path(sys.argv[2])
texts = {p.stem: p.read_text(encoding="utf-8") for p in text_dir.glob("L*.txt")}
num = re.compile(r"\d+(?:\.\d+)?")
misses = 0
for card in cards:
    lesson = texts[card["lesson"]]
    for field in ("front", "back"):
        for token in num.findall(card[field]):
            if token not in lesson:
                misses += 1
                print(f"{card['id']} {card['lesson']} {field}: '{token}' not in lesson text")
print("tokens missing:", misses, "cards:", len(cards))
