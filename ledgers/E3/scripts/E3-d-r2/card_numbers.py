"""Lists the numbers on each card that do not occur literally in its own lesson (tag-stripped text), round 2.

Usage (from the checkout): .venv/bin/python ledgers/E3/scripts/E3-d-r2/card_numbers.py
"""

from __future__ import annotations

import html
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parents[4] / "course" / "modules" / "E" / "E3"


def main() -> None:
    cards = json.loads((BASE / "cards.json").read_text(encoding="utf-8"))
    cache: dict[str, str] = {}
    misses = []
    for card in cards:
        lesson = card["lesson"]
        if lesson not in cache:
            raw = (BASE / f"{lesson}.html").read_text(encoding="utf-8")
            cache[lesson] = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", raw))).replace(",", "")
        for number in set(re.findall(r"(?<![A-Za-z_])\d+(?:\.\d+)?", card["back"] + " " + card["front"])):
            if number in ("0", "1", "2", "3", "4", "5"):
                continue
            if number not in cache[lesson]:
                misses.append((card["id"], lesson, number))
    print("numbers not literally in own lesson:", misses)


if __name__ == "__main__":
    main()
