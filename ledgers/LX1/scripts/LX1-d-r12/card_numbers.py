"""For every LX1 card, list each number in its front or back and whether that exact token appears in the
plain text of the card's own lesson page (tags stripped, entities unescaped, MathJax markup left in place).

Run with: python3 -I -W error ledgers/LX1/scripts/LX1-d-r12/card_numbers.py course/modules/LX/LX1
"""

import html
import json
import re
import sys
from pathlib import Path

unit_dir = Path(sys.argv[1])
cards = json.loads((unit_dir / "cards.json").read_text(encoding="utf-8"))


def page_text(name: str) -> str:
    raw = (unit_dir / f"{name}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<(?=/?[a-zA-Z!])[^>]*>", " ", raw)
    return html.unescape(raw)


pages = {lesson: page_text(lesson) for lesson in ("L01", "L02", "L03", "L04")}
pages_all = "\n".join(pages.values())
NUM = re.compile(r"(?<![A-Za-z_])\d+(?:[.,/]\d+)*")
missing = []
checked = 0
for card in cards:
    text = card["front"] + " " + card["back"]
    for tok in sorted(set(NUM.findall(text))):
        if tok in {"0", "1", "2", "3"} and len(tok) == 1:
            continue
        checked += 1
        if tok not in pages[card["lesson"]]:
            where = "elsewhere in unit" if tok in pages_all else "NOT in unit"
            missing.append((card["id"], card["lesson"], tok, where))
print("number tokens checked", checked)
print("tokens absent from the card's own lesson", len(missing))
for m in missing:
    print("  ", m)
