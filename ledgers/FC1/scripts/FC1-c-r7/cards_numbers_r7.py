"""Round-6 check: every number in a card's front or back appears in the card's lesson text (lessons stripped by strip_html_r6.py).

Usage: python -I cards_numbers_r6.py <cards.json> <dir with L01.txt..L05.txt>
"""
import json
import re
import pathlib
import sys

cards = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
lessons = {p.stem: p.read_text(encoding="utf-8").replace(",", "") for p in pathlib.Path(sys.argv[2]).glob("L0*.txt")}
issues = []
for card in cards:
    body = lessons[card["lesson"]]
    for field in ("front", "back"):
        for number in re.findall(r"\d+(?:\.\d+)?", card[field].replace(",", "")):
            if number not in body:
                issues.append((card["id"], field, number))
from collections import Counter
print("cards", len(cards), "unique ids", len({c["id"] for c in cards}), "number issues", len(issues))
print("duplicate fronts", [k for k, v in Counter(c["front"] for c in cards).items() if v > 1], "duplicate backs", [k for k, v in Counter(c["back"] for c in cards).items() if v > 1])
for issue in issues:
    print(issue)
