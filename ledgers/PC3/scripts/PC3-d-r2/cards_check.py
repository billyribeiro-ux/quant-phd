"""Structural and numeric checks of course/modules/PC/PC3/cards.json against the six lesson text dumps.

usage: python -I cards_check.py <checkout-root> <scratch-dir-with L01..L06.txt>
Prints: id/schema checks, duplicate-front/back scan (difflib ratio > 0.6), grade/basis presence, and for every
number token in a card back (after normalising '−' and thousands spaces) whether it occurs in the card's own lesson dump
or in any lesson dump. Numbers found in no lesson are listed for manual review.
"""
import difflib
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
cards = json.loads((root / "course/modules/PC/PC3/cards.json").read_text(encoding="utf-8"))
print(f"cards: {len(cards)}")
ids = [c["id"] for c in cards]
expected = [f"PC3-c{i:03d}" for i in range(1, len(cards) + 1)]
print("ids unique:", len(set(ids)) == len(ids), "| sequential c001..c%03d:" % len(cards), sorted(ids) == expected)
print("file order equals id order:", ids == expected)
keyset = {frozenset(c.keys()) for c in cards}
print("key sets:", [sorted(k) for k in keyset])
print("cite empty on all:", all(c.get("cite") == [] for c in cards))
lessons = {}
for L in ["L01", "L02", "L03", "L04", "L05", "L06"]:
    lessons[L] = (scratch / f"{L}.txt").read_text(encoding="utf-8")
per = {}
for c in cards:
    per[c["lesson"]] = per.get(c["lesson"], 0) + 1
print("cards per lesson:", dict(sorted(per.items())))
for c in cards:
    g = c.get("grade")
    if g in ("T", "C") and not c.get("basis"):
        print("MISSING BASIS", c["id"], g)
    if g not in (None, "T", "C"):
        print("BAD GRADE", c["id"], g)
    if g is None and c.get("basis") is not None:
        print("BASIS WITHOUT GRADE", c["id"])
print("--- duplicate scan (front or back similarity > 0.6) ---")
for i in range(len(cards)):
    for j in range(i + 1, len(cards)):
        a, b = cards[i], cards[j]
        rf = difflib.SequenceMatcher(None, a["front"], b["front"]).ratio()
        rb = difflib.SequenceMatcher(None, a["back"], b["back"]).ratio()
        if rf > 0.6 or rb > 0.6:
            print(f"{a['id']} {b['id']} front={rf:.2f} back={rb:.2f}")
print("--- numbers in card backs and fronts not found in any lesson dump (normalised) ---")
alltext = "\n".join(lessons.values())


def norm(s: str) -> str:
    return s.replace("−", "-").replace(" ", "").replace(" ", "")


nalltext = norm(alltext)
num = re.compile(r"-?\d[\d,]*(?:\.\d+)?(?:/\d+)?")
for c in cards:
    for field in ("front", "back"):
        for tok in num.findall(c[field]):
            t = tok.rstrip(",")
            if t.lstrip("-") in ("1", "2", "3", "0"):
                continue
            if norm(t) not in nalltext and norm(t.replace(",", "")) not in nalltext:
                print(c["id"], field, repr(tok))
