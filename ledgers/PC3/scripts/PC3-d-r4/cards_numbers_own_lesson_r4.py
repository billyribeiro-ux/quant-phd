"""Round-4 check: every number token in a card's front or back must occur in that card's own lesson dump
(normalised: '−' to '-', thin/regular spaces removed, thousands commas and spaces ignored), and near-duplicate
scan (difflib ratio > 0.6 on fronts or backs) over all cards.

usage: python -I cards_numbers_own_lesson_r4.py <checkout-root> <scratch-dir-with-L01..L06.txt>
"""
import difflib
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
cards = json.loads((root / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
lessons = {L: (scratch / f"{L}.txt").read_text(encoding="utf-8") for L in ["L01", "L02", "L03", "L04", "L05", "L06"]}


def norm(s: str) -> str:
    return s.replace("−", "-").replace(" ", "").replace(" ", "").replace(" ", "").replace(",", "").replace("\\", "")


normed = {L: norm(t) for L, t in lessons.items()}
num = re.compile(r"-?\d[\d,]*(?:\.\d+)?(?:/\d+)?")
flagged = []
for c in cards:
    own = normed[c["lesson"]]
    for field in ("front", "back"):
        for tok in num.findall(c[field]):
            t = norm(tok).rstrip(".")
            if t.lstrip("-") in ("0", "1", "2", "3", "10", "100") and t.lstrip("-") != "":
                # small integers are checked by the lesson text too, but are too common to flag alone
                pass
            if t not in own:
                flagged.append((c["id"], c["lesson"], field, tok))
print("number tokens not in own lesson:", len(flagged))
for item in flagged:
    print("  ", item)
print("--- near-duplicates (front or back difflib ratio > 0.6) ---")
dups = 0
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if rf > 0.6 or rb > 0.6:
            dups += 1
            print(f"{a['id']} {b['id']} front={rf:.2f} back={rb:.2f}")
print("pairs:", dups)
print("--- cards whose basis mentions Lab 1 but grade is T (checked) ---")
for c in cards:
    if c.get("grade") == "T" and "Lab" in (c.get("basis") or ""):
        print("  ", c["id"], c["basis"][:140])
print("--- grade C cards whose basis names no Lab/Problem/Remark/Example ---")
for c in cards:
    if c.get("grade") == "C" and not re.search(r"Lab|Problem|Remark|Example", c.get("basis") or ""):
        print("  ", c["id"], c.get("basis"))
