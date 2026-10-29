"""Coverage of named results by cards: every Definition, Theorem, Proposition, Corollary, Lemma and Remark heading
in each lesson (from the lesson's text) and whether some card of that lesson names it. Usage:
.venv/bin/python -I ledgers/E3/scripts/E3-d-r4/card_coverage.py
"""
import json
import re
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).resolve().parents[4] / "course" / "modules" / "E" / "E3"


class _Text(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.parts: list[str] = []

    def handle_data(self, data: str) -> None:
        self.parts.append(data)


cards = json.loads((BASE / "cards.json").read_text(encoding="utf-8"))
total_missing = 0
for lesson in ["L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08"]:
    p = _Text()
    p.feed((BASE / f"{lesson}.html").read_text(encoding="utf-8"))
    text = re.sub(r"\s+", " ", " ".join(p.parts))
    names = sorted(set(re.findall(r"\b(Definition|Theorem|Proposition|Corollary|Lemma|Remark) (\d+\.\d+)\b", text)))
    lesson_cards = " ".join(c["front"] + " " + c["back"] for c in cards if c["lesson"] == lesson)
    missing = [f"{k} {n}" for k, n in names if not re.search(rf"\b{k} {re.escape(n)}\b", lesson_cards)]
    total_missing += len(missing)
    print(f"{lesson}: {len(names)} named results, {len(names) - len(missing)} named by a card of the lesson; not named: {missing}")
print("total named results not named by any card of their lesson:", total_missing)
