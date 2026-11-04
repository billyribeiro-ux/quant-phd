"""Slice e check: each numeric token in a card (fraction, decimal, e-notation) must be printed in the card's lesson.

Usage: python -I card_numbers.py <cards.json> <lesson-text-dir>
Tokens printed only in another E4 lesson, or in LaTeX form (e.g. \\tfrac{3}{32}), are reported as OTHER.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

TOKEN = re.compile(r"(?<![A-Za-z_\d.])(\d+/\d+|\d+\.\d+(?:e-?\d+)?|\d+e-\d+)(?!\d)")


def main() -> None:
    cards = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    texts = {p.stem: p.read_text(encoding="utf-8") for p in Path(sys.argv[2]).glob("*.txt")}
    missing = 0
    checked = 0
    for card in cards:
        lesson_text = texts.get(card["lesson"], "")
        for token in sorted(set(TOKEN.findall(card["front"] + " " + card["back"]))):
            checked += 1
            if token in lesson_text:
                continue
            where = [name for name, text in texts.items() if token in text]
            if where:
                print(f"OTHER {card['id']} ({card['lesson']}): '{token}' printed only in {sorted(where)}")
            else:
                missing += 1
                print(f"MISSING {card['id']} ({card['lesson']}): '{token}' in no E4 lesson text")
    print(f"numeric tokens checked={checked} missing={missing}")


if __name__ == "__main__":
    main()
