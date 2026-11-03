"""Round 3 verifier: cards.json scan for E5 (all 139 cards for duplicates, the 58 L04-L06 cards for lesson agreement).

Checks: unique ids; no duplicate fronts or backs (after lower-casing and stripping punctuation); every card's
lesson field; every number token in a card's back occurs in the card's own lesson page (tags stripped, entities
unescaped), so that a number on a card is a number the lesson states. A miss is printed for a manual reading;
the manual reading of every L04-L06 card is recorded in the fragment.
Run: .venv/bin/python -I ledgers/E5/scripts/E5-b-r3/d3_cards_b.py
"""

from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
E5 = ROOT / "course" / "modules" / "E" / "E5"
cards = json.loads((E5 / "cards.json").read_text(encoding="utf-8"))
print("cards total", len(cards), "unique ids", len({c["id"] for c in cards}))


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9 ]+", "", s.lower()).strip()


fronts = Counter(norm(c["front"]) for c in cards)
backs = Counter(norm(c["back"]) for c in cards)
print("duplicate fronts", [k for k, v in fronts.items() if v > 1])
print("duplicate backs", [k for k, v in backs.items() if v > 1])

lesson_text: dict[str, str] = {}
for lesson in ("L04", "L05", "L06"):
    raw = (E5 / f"{lesson}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<[^>]+>", " ", raw)
    lesson_text[lesson] = html.unescape(raw)

misses = 0
sub = [c for c in cards if c["lesson"] in lesson_text]
print("L04-L06 cards", len(sub), Counter(c["lesson"] for c in sub))
for c in sub:
    nums = set(re.findall(r"\d+(?:\.\d+)?(?:/\d+)?", c["back"]))
    text = lesson_text[c["lesson"]]
    missing = sorted(n for n in nums if n not in text and not (n.isdigit() and len(n) == 1))
    if missing:
        misses += 1
        print("NUMBER-NOT-IN-LESSON", c["id"], missing)
print("cards with a number absent from their lesson:", misses)

# Ids and lesson fields: the id stays in the unit prefix and the lesson field is a real lesson page
for c in cards:
    assert c["id"].startswith("E5-c"), c["id"]
    assert (E5 / f"{c['lesson']}.html").exists(), c["id"]
print("ids and lesson fields well formed")
sys.exit(0)
