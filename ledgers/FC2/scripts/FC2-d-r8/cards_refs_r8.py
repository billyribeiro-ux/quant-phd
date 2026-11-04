"""For every FC2 card: each numbered reference (Definition/Proposition/Theorem/Lemma/Corollary/Remark/Example x.y, A1-A8)
must appear in the card's own lesson HTML, and the card's lesson must be one of L01-L08. Also prints duplicate fronts.

Usage: python -I cards_refs_r8.py <FC2 dir>
"""
import collections
import json
import re
import sys
from pathlib import Path

d = Path(sys.argv[1])
cards = json.loads((d / "cards.json").read_text(encoding="utf-8"))
lesson_text = {}
for p in d.glob("L0*.html"):
    lesson_text[p.stem] = p.read_text(encoding="utf-8")
bad = 0
pat = re.compile(r"\b(Definition|Proposition|Theorem|Lemma|Corollary|Remark|Example|Assumption|Section)\s+(\d+(?:\.\d+)?)\b|\b(A\d)\b")
fronts = collections.Counter(c["front"] for c in cards)
for f, n in fronts.items():
    if n > 1:
        print("DUP FRONT", n, f)
for c in cards:
    text = c["front"] + " " + c["back"]
    lesson = lesson_text.get(c["lesson"])
    if lesson is None:
        print("NO LESSON", c["id"], c["lesson"]); bad += 1; continue
    for m in pat.finditer(text):
        token = m.group(0)
        if m.group(3):
            needle = m.group(3)
            ok = re.search(rf"\b{needle}\b", lesson) is not None
            # a card may cite A-numbers of another lesson only when it says so; flag for manual look
            if not ok:
                print("MISSING", c["id"], c["lesson"], repr(token)); bad += 1
            continue
        kind, num = m.group(1), m.group(2)
        if kind == "Section":
            continue
        if re.search(rf"{kind}\s+{re.escape(num)}\b", lesson) is None:
            print("CHECK", c["id"], c["lesson"], repr(token), "not found in own lesson")
print("cards", len(cards), "flags", bad)
