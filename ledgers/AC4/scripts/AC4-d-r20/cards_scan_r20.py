"""Round 20: duplicate scan and lesson-coverage scan of AC4 flashcards for L07 and L08, and card-to-text checks."""

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1])
cards = json.loads((ROOT / "course/modules/AC/AC4/cards.json").read_text(encoding="utf-8"))
ids = Counter(c["id"] for c in cards)
fronts = Counter(c["front"].strip().lower() for c in cards)
backs = Counter(c["back"].strip().lower() for c in cards)
print("cards", len(cards), "duplicate ids", [k for k, v in ids.items() if v > 1])
print("duplicate fronts", [k for k, v in fronts.items() if v > 1])
print("duplicate backs", [k for k, v in backs.items() if v > 1])
for lesson in ("L07", "L08"):
    sel = [c["id"] for c in cards if c["lesson"] == lesson]
    print(lesson, len(sel), sel)
bad_lesson = [c["id"] for c in cards if c["id"][-3:].isdigit() and c["id"] >= "AC4-c082" and c["id"] <= "AC4-c134" and c["lesson"] not in ("L07", "L08")]
print("cards in the 082-134 range whose lesson is not L07/L08:", bad_lesson)
for c in cards:
    if c["id"] in ("AC4-c095", "AC4-c089", "AC4-c096"):
        print(c["id"], "basis" , c.get("basis"), "| grade", c.get("grade"))
# every card of grade C must carry a basis; every grade T card must not claim a SIMULATED basis
print("grade C without basis:", [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")])
print("basis mentions 'exact-check':", [c["id"] for c in cards if "exact-check" in c.get("basis", "")])
