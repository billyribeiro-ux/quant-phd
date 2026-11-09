"""Round 3 FC2-a: card scan for L01-L03 (numbers on each card occur in its lesson; duplicates; grade/basis; ids)."""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ROOT / "course/modules/FC/FC2"
cards = json.loads((PAGES / "cards.json").read_text(encoding="utf-8"))
print("cards total", len(cards), "distinct ids", len({c["id"] for c in cards}))
fronts = Counter(c["front"] for c in cards)
backs = Counter(c["back"] for c in cards)
print("duplicate fronts", [f for f, n in fronts.items() if n > 1])
print("duplicate backs", [b for b, n in backs.items() if n > 1])
per = Counter(c["lesson"] for c in cards)
print("per lesson", dict(sorted(per.items())))
lesson_text = {}
for L in ["L01", "L02", "L03"]:
    lesson_text[L] = html.unescape((PAGES / f"{L}.html").read_text(encoding="utf-8"))
NUM = re.compile(r"(?<![A-Za-z_])\d+(?:[.,]\d+)*")
bad = 0
for c in cards:
    if c["lesson"] not in lesson_text:
        continue
    text = lesson_text[c["lesson"]]
    nums = set(NUM.findall(c["front"] + " " + c["back"]))
    missing = [n for n in nums if n not in text and n.replace(",", "") not in text]
    if missing:
        bad += 1
        print("NUMBER NOT IN LESSON", c["id"], c["lesson"], missing)
    if c.get("grade") == "T" and not c.get("basis"):
        print("T without basis", c["id"])
    if c.get("grade") in ("C", "B", "A") and not c.get("basis") and not c.get("cite"):
        print("graded without basis/cite", c["id"])
print("cards with a number absent from lesson:", bad)
