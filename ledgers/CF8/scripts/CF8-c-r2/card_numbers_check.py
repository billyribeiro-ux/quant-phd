"""Check that every number on a card's back appears in its cited lesson (round 2, CF8-c).

Usage: .venv/bin/python ledgers/CF8/scripts/CF8-c-r2/card_numbers_check.py
Prints the numbers found in no lesson text (the two hits are LaTeX {,} grouping: 608{,}065 and 1{,}488{,}640 in L04).
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

UNIT = Path(__file__).resolve().parents[4] / "course" / "modules" / "CF" / "CF8"


def main() -> None:
    cards = json.loads((UNIT / "cards.json").read_text(encoding="utf-8"))
    plain = {}
    for lesson in ("L01", "L02", "L03", "L04", "L05"):
        raw = (UNIT / f"{lesson}.html").read_text(encoding="utf-8")
        plain[lesson] = html.unescape(re.sub(r"<[^>]+>", " ", raw)).replace("{,}", ",")
    missing = []
    for card in cards:
        src = plain[card["lesson"]]
        for number in re.findall(r"\d[\d,]*(?:\.\d+)?", card["back"]):
            bare = number.replace(",", "")
            if bare in {"0", "1", "2", "3", "5", "7", "10", "12", "13", "14", "20", "30", "45", "50", "60", "90", "100", "365"}:
                continue
            if number not in src and bare not in src:
                missing.append((card["id"], card["lesson"], number))
    print(f"cards {len(cards)}; numbers not found in the cited lesson: {missing}")


if __name__ == "__main__":
    main()
