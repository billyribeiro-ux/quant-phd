"""Verifier M7 slice a round 1: structural and number checks on course/modules/M/M7/cards.json.

Reads cards.json and the lesson pages as text. Prints the L01-L03 inventory, duplicate checks over the whole
file, grade counts, the card number citations found in each card and whether each cited number occurs in the
card's own lesson page, and the full text of every card that changed since the base pin (passed as ids).
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/Users/billyribeiro/.fanout/wt/verifyF21-M7-a")
M7 = ROOT / "course/modules/M/M7"
cards = json.loads((M7 / "cards.json").read_text(encoding="utf-8"))
print("total cards in file:", len(cards))
ids = [c["id"] for c in cards]
dupe_ids = [k for k, v in Counter(ids).items() if v > 1]
print("duplicate ids over whole file:", dupe_ids)
fronts = Counter(c["front"].strip().lower() for c in cards)
print("duplicate fronts over whole file:", [k for k, v in fronts.items() if v > 1])
keys = Counter(tuple(sorted(c.keys())) for c in cards)
print("key sets:", dict(keys))
bad_grade = [c["id"] for c in cards if c.get("grade") not in ("T", "C")]
print("cards with grade not T/C:", bad_grade)
no_basis_c = [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")]
print("C cards without basis:", no_basis_c)
basis_t = [c["id"] for c in cards if c.get("grade") == "T" and c.get("basis")]
print("T cards with basis:", basis_t)
lessons = Counter(c["lesson"] for c in cards)
print("cards per lesson:", dict(sorted(lessons.items())))

scope = [c for c in cards if c["lesson"] in ("L01", "L02", "L03")]
print("L01-L03 cards:", len(scope), "grades:", dict(Counter(c["grade"] for c in scope)))
for L in ("L01", "L02", "L03"):
    sub = [c for c in scope if c["lesson"] == L]
    print(L, len(sub), dict(Counter(c["grade"] for c in sub)), sub[0]["id"], "...", sub[-1]["id"])

# every number citation in each card must occur in its lesson page
cite_re = re.compile(r"\b(Definition|Proposition|Theorem|Lemma|Remark|Example|Assumption|Section|Part|Lab|Corollary|Problem|Exercise)\s+(\d+(?:\.\d+)?|[A-Z])\b")
for c in scope:
    page = (M7 / f"{c['lesson']}.html").read_text(encoding="utf-8")
    text = c["front"] + " " + c["back"]
    for kind, num in cite_re.findall(text):
        token = f"{kind} {num}"
        if token not in page and token.replace("Lab ", "Lab ") not in page:
            print("CITATION NOT IN LESSON:", c["id"], c["lesson"], repr(token))

want = sys.argv[1:]
for c in cards:
    if c["id"] in want:
        print("----", c["id"], c["lesson"], c["grade"], c.get("basis"))
        print("FRONT:", c["front"])
        print("BACK:", c["back"])
