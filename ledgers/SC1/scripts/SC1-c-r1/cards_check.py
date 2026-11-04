"""Card checks for L07 and L08 cards in course/modules/SC/SC1/cards.json (verifier round 1, slice c).

Usage: python -I ledgers/SC1/scripts/SC1-c-r1/cards_check.py   (run from the checkout root; reads only)
Checks: duplicate fronts and backs across the whole deck; every number in an L07/L08 card back appears in its lesson;
cards whose text uses the T symbol for a first-passage index; cards that repeat 'continuity ... from above'.
"""

from __future__ import annotations

import collections
import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SC1 = ROOT / "course/modules/SC/SC1"


def norm(s: str) -> str:
    return re.sub(r"\W+", " ", s).strip().lower()


def main() -> None:
    cards = json.loads((SC1 / "cards.json").read_text(encoding="utf-8"))
    print("cards:", len(cards), "lessons:", dict(collections.Counter(c["lesson"] for c in cards)))
    fronts = collections.Counter(norm(c["front"]) for c in cards)
    backs = collections.Counter(norm(c["back"]) for c in cards)
    print("duplicate fronts:", sum(1 for v in fronts.values() if v > 1), "duplicate backs:", sum(1 for v in backs.values() if v > 1))
    print("duplicate ids:", len(cards) - len({c["id"] for c in cards}))
    lesson_text = {
        p: html.unescape(re.sub(r"<[^>]+>", " ", (SC1 / f"{p}.html").read_text(encoding="utf-8"))) for p in ("L07", "L08")
    }
    for c in cards:
        if c["lesson"] not in lesson_text:
            continue
        nums = set(re.findall(r"\d+\.\d+|\b\d{2,}\b", c["back"]))
        missing = sorted(n for n in nums if n not in lesson_text[c["lesson"]])
        if missing:
            print("number not in lesson:", c["id"], missing)
    print("T symbol in card text (L07/L08):")
    for c in cards:
        if c["lesson"] in lesson_text and re.search(r"T_|T\(|T_\{|min\(T", c["front"] + " " + c["back"]):
            print("  ", c["id"], c["lesson"])
    print("'from above' continuity in card back (L07/L08):")
    for c in cards:
        if c["lesson"] in lesson_text and re.search(r"from above", c["back"] + c["front"], re.I):
            print("  ", c["id"], "|", c["back"][:120])


if __name__ == "__main__":
    main()
