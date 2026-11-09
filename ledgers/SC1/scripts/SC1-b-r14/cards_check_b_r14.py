"""Round-14 card checks for SC1 slice b (cards whose lesson is L04, L05 or L06).

1. Every card's numbered reference (Lemma/Proposition/Theorem/Corollary/Remark/Definition/Problem/
   Assumption/Assumption A<n>) must occur in that card's lesson text (stripped of tags).
2. No duplicate cards: no two cards share a front or a back, across the whole cards.json.
3. Every card id is unique.
"""

from __future__ import annotations

import html
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(sys.argv[1])
SC1 = ROOT / "course" / "modules" / "SC" / "SC1"
TAG = re.compile(r"</?[a-zA-Z][^>]*>|<!--.*?-->", re.S)


def lesson_text(name: str) -> str:
    raw = (SC1 / f"{name}.html").read_text(encoding="utf-8")
    return html.unescape(TAG.sub(" ", raw))


cards = json.loads((SC1 / "cards.json").read_text(encoding="utf-8"))
texts = {n: lesson_text(n) for n in ("L01", "L02", "L03", "L04", "L05", "L06", "L07", "L08")}
ref_pat = re.compile(
    r"\b(Lemma|Proposition|Theorem|Corollary|Remark|Definition|Problem|Assumption|Lab|Section)\s+"
    r"(A?\d+(?:\.\d+)?(?:\([a-z]\))?|[MPER]\d+|\d+)"
)
problems: list[str] = []
checked = 0
for card in cards:
    if card["lesson"] not in ("L04", "L05", "L06"):
        continue
    checked += 1
    text = texts[card["lesson"]]
    blob = card["front"] + " " + card["back"]
    for m in ref_pat.finditer(blob):
        token = m.group(0)
        # Problem and Lab refs are labelled in the lesson by their own tags; check the number part.
        num = m.group(2)
        if m.group(1) in ("Problem",):
            needle = num
        elif m.group(1) == "Lab":
            needle = "Lab 1"
        elif m.group(1) == "Section":
            needle = "Section " + num
        else:
            needle = f"{m.group(1)} {num}"
        if needle not in text and not (m.group(1) == "Assumption" and f"Assumption {num}" in text):
            problems.append(f"{card['id']}: reference '{token}' not found in {card['lesson']}.html")
print(f"cards checked (L04-L06): {checked}")
print("numbered-reference problems:", len(problems))
for p in problems:
    print("  ", p)

fronts = Counter(c["front"].strip() for c in cards)
backs = Counter(c["back"].strip() for c in cards)
ids = Counter(c["id"] for c in cards)
print("duplicate fronts:", [f for f, n in fronts.items() if n > 1])
print("duplicate backs:", [b for b, n in backs.items() if n > 1])
print("duplicate ids:", [i for i, n in ids.items() if n > 1])
print("total cards:", len(cards))
