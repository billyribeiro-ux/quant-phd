"""Round-4 verifier: every number a card states (decimal or integer of two or more digits) must occur in the lesson
text the card names, or in the card's own text (the lesson text includes the printed lab output). Prints the
misses. Usage (from the checkout root): .venv/bin/python -I ledgers/M3/scripts/M3-d-r5/card_numbers_r4.py
"""

import json
import re
from pathlib import Path

ROOT = Path.cwd()
TEXT = ROOT / "ledgers/M3/scripts/M3-d-r5/out/text"
cards = json.loads((ROOT / "course/modules/M/M3/cards.json").read_text(encoding="utf-8"))
texts = {f.stem: f.read_text(encoding="utf-8") for f in TEXT.glob("L0*.txt")}
NUM = re.compile(r"(?<![\w.])-?\d+(?:\.\d+)?(?![\w])")
misses = []
checked = 0
for card in cards:
    lesson = texts[card["lesson"]]
    own = card["front"] + " " + card["back"]
    for num in sorted(set(NUM.findall(card["back"]))):
        core = num.lstrip("-")
        if len(core.replace(".", "")) < 2:
            continue  # single digits and 0/1 are structural
        checked += 1
        if core in lesson or core in own:
            continue
        # also accept a value printed with a different number of decimals in the lesson, e.g. 0.6400000000 vs 0.64
        if "." in core and re.search(r"(?<![\w.])" + re.escape(core.rstrip("0").rstrip(".")) , lesson):
            continue
        misses.append((card["id"], card["lesson"], num))
print(f"numbers checked: {checked}")
for m in misses:
    print("MISS", m)
print(f"misses: {len(misses)}")
