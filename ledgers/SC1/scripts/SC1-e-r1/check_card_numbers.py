"""For every card, check that each numeric token in front/back appears verbatim in its lesson's
visible text (extracted by extract_text.py, which keeps lab output blocks) or raw HTML.
Read-only. Usage: check_card_numbers.py <cards.json> <module dir>
"""
import json
import re
import sys

import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from extract_text import page_text

cards_path, module_dir = sys.argv[1], sys.argv[2]
cards = json.load(open(cards_path, encoding="utf-8"))
NUM = re.compile(r"(?<![A-Za-z_\-])\d+(?:\.\d+)?(?:[eE][-+]?\d+)?")
cache: dict[str, str] = {}


def corpus(lesson: str) -> str:
    if lesson not in cache:
        text = page_text(f"{module_dir}/{lesson}.html")
        raw = open(f"{module_dir}/{lesson}.html", encoding="utf-8").read()
        cache[lesson] = text + "\n" + raw
    return cache[lesson]


missing = []
total = 0
for c in cards:
    body = c["front"] + " " + c["back"]
    for tok in sorted(set(NUM.findall(body))):
        total += 1
        if tok not in corpus(c["lesson"]):
            missing.append((c["id"], c["lesson"], tok))
print(f"numeric tokens checked: {total}")
print(f"tokens not found verbatim in their lesson: {len(missing)}")
for row in missing:
    print("  MISSING", *row)
