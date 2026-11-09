"""Round 18: card inventory for lessons L01, L03, L04 (course/modules/LX/LX1/cards.json).

Prints, per card, its id, lesson, grade/basis fields, and checks: unique ids, lesson in {L01..L04}, every card that
carries a grade has a basis, and the count per lesson. Run from the checkout root with .venv/bin/python -I.
"""
import json
from collections import Counter

cards = json.load(open("course/modules/LX/LX1/cards.json", encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards:", len(cards), "unique ids:", len(set(ids)) == len(ids))
print("per lesson:", dict(Counter(c["lesson"] for c in cards)))
bad = [c["id"] for c in cards if "grade" in c and not c.get("basis")]
print("graded cards without basis:", bad)
for c in cards:
    if c["lesson"] in ("L01", "L03", "L04"):
        extra = {k: c[k] for k in ("grade", "basis") if k in c}
        print(c["id"], c["lesson"], "|", c["front"][:150].replace("\n", " "), "|", extra)
