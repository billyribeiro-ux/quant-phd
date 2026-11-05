"""Round-10 card checks for FC1 (verifier): duplicates, card numbers in the card's own lesson, numbered citations.

Usage: python -I ledgers/FC1/scripts/FC1-c-r11/cards_check_r10.py   (needs out/lessons/*.txt from lesson_text.py)
"""

from __future__ import annotations

import json
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CARDS = json.loads((ROOT / "course" / "modules" / "FC" / "FC1" / "cards.json").read_text(encoding="utf-8"))
LESSONS = ROOT / "ledgers" / "FC1" / "scripts" / "FC1-c-r11" / "out" / "lessons"
texts = {f"L0{i}": (LESSONS / f"L0{i}.txt").read_text(encoding="utf-8") for i in range(1, 6)}

ids = [c["id"] for c in CARDS]
print("cards:", len(CARDS), "unique ids:", len(set(ids)))
print("duplicate fronts:", len(CARDS) - len({c["front"] for c in CARDS}))
print("duplicate backs:", len(CARDS) - len({c["back"] for c in CARDS}))
near = []
for i, a in enumerate(CARDS):
    for b in CARDS[i + 1 :]:
        r = SequenceMatcher(None, a["front"], b["front"]).ratio()
        if r > 0.8:
            near.append((round(r, 3), a["id"], b["id"], a["front"][:60], b["front"][:60]))
print("near-duplicate fronts (ratio > 0.8):", len(near))
for n in near:
    print("  ", n)
missing_numbers = []
for c in CARDS:
    lesson = texts[c["lesson"]]
    for num in set(re.findall(r"\d[\d,]*(?:\.\d+)?", c["back"] + " " + c["front"])):
        digits = num.replace(",", "")
        if digits.replace(".", "").isdigit() and float(digits) >= 13 and num not in lesson and digits not in lesson:
            missing_numbers.append((c["id"], num))
print("card numbers >= 13 absent from the card's lesson:", missing_numbers)
cites = []
for c in CARDS:
    for ref in re.findall(r"\((?:[^()]*?)(Definition|Proposition|Remark|Example|Corollary|Section|Problem|Assumption|Lab)[^()]*\)", c["back"]):
        cites.append(c["id"])
print("cards with a bracketed citation:", len(set(cites)))
for c in CARDS:
    if c["id"] in ("FC1-c064", "FC1-c101", "FC1-c150", "FC1-c152", "FC1-c009"):
        print("CHANGED", c["id"], c["lesson"], c.get("grade"), c["back"])
