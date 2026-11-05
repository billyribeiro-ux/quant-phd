"""LX1-b round 11: dump the L03/L04 cards, check ids and fronts for duplicates, and check each card's numbers appear in its lesson.

Usage: python -I ledgers/LX1/scripts/LX1-b-r11/cards_r11.py <checkout>
"""

import collections
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
cards = json.loads((root / "course/modules/LX/LX1/cards.json").read_text(encoding="utf-8"))
ids = collections.Counter(c["id"] for c in cards)
fronts = collections.Counter(c["front"] for c in cards)
print("cards total:", len(cards), "lessons:", dict(collections.Counter(c["lesson"] for c in cards)))
print("duplicate ids:", [k for k, v in ids.items() if v > 1])
print("duplicate fronts:", [k for k, v in fronts.items() if v > 1])
pages = {lesson: (root / f"course/modules/LX/LX1/{lesson}.html").read_text(encoding="utf-8") for lesson in ("L03", "L04")}
subset = [c for c in cards if c["lesson"] in pages]
print("L03/L04 cards:", len(subset), "(L03:", sum(c["lesson"] == "L03" for c in subset), "L04:", sum(c["lesson"] == "L04" for c in subset), ")")
numbers = re.compile(r"\d[\d,]*\.\d+|\d{4}-\d{2}|\b\d{3,}\b")
for c in subset:
    print(f"{c['id']} {c['lesson']} grade={c.get('grade')} front={c['front']}")
    print(f"    back={c['back']}")
    print(f"    basis={c.get('basis')}")
    for num in sorted(set(numbers.findall(c["back"]))):
        if num not in pages[c["lesson"]]:
            print(f"    NOT IN LESSON: {num}")
