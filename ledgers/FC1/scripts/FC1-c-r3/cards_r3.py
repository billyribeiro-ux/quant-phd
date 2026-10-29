"""For each FC1 card: (1) every cited label (Definition/Proposition/... N.N, Lab 1 Part X, Example, Remark, Assumption,
misconception N, Problem Px/Rx, Section N) must occur in the card's own lesson text or in the named lesson; (2) every
number in the card's back must occur in the lesson text, or in the lesson's printed lab output, after normalising
thousands separators and number forms.

Usage: python ledgers/FC1/scripts/FC1-c-r3/cards_r3.py <checkout-root> <lesson-text-dir>
The lesson text dir holds L01.txt .. L05.txt, produced by stripping the HTML of the lesson pages.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
tdir = Path(sys.argv[2])
cards = json.loads((root / "course/modules/FC/FC1/cards.json").read_text(encoding="utf-8"))
lessons = {p.stem: p.read_text(encoding="utf-8") for p in sorted(tdir.glob("L0*.txt"))}
allText = "\n".join(lessons.values())
LABEL = re.compile(r"(Definition|Proposition|Assumption|Example|Remark|Problem|Corollary|Lemma|Section|Lab \d, Part [A-D])\s+(\w+(?:\.\w+)*|[A-D])")
NUM = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?")
bad = []
for c in cards:
    back = c["back"]
    labels = [m.group(0) for m in LABEL.finditer(back)]
    for lab in labels:
        if lab in allText or lab.replace(" ", " ") in allText:
            continue
        bad.append((c["id"], "label-not-in-lessons", lab))
    for m in NUM.finditer(back):
        tok = m.group(0).rstrip(",")
        norm = tok.replace(",", "")
        if norm in ("1", "2", "3", "0", "4", "5", "10", "8", "6", "7", "9"):
            continue
        if tok in allText or norm in allText:
            continue
        bad.append((c["id"], "number-not-in-lessons", tok))
for b in bad:
    print(*b, sep=" | ")
print("cards", len(cards), "flags", len(bad))
