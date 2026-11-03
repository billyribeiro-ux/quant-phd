"""For every card, list each numeric token in front/back that does not occur in the card's own lesson page.

Usage: python -I v3_card_numbers_in_lesson.py  (verifier round 3, slice e). Numbers are matched as whole tokens
in the raw HTML of the lesson (KaTeX source included). A miss is a candidate defect to read by hand.
"""
import html
import json
import re
from pathlib import Path

cards = json.load(open("course/modules/M/M7/cards.json", encoding="utf-8"))
pages = {}
for n in range(1, 9):
    raw = Path(f"course/modules/M/M7/L{n:02d}.html").read_text(encoding="utf-8")
    pages[f"L{n:02d}"] = html.unescape(raw)
# labs whose output is embedded are also in the page; include twin outputs for the lab-result cards
num = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?")
missing = []
for c in cards:
    text = pages[c["lesson"]]
    for field in ("front", "back", "basis"):
        for tok in num.findall(c.get(field, "")):
            if not re.search(r"(?<![\d.])" + re.escape(tok) + r"(?![\d])", text):
                missing.append((c["id"], field, tok))
print("numeric tokens not found in own lesson page:", len(missing))
for m in missing:
    print(" ", m)
