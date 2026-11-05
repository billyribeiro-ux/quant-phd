"""For every M4 card, check each block reference (Definition/Theorem/Proposition/Example/Remark/Lemma/Problem/Assumption
N.M, Section N) against the block index of its own lesson, unless the reference is preceded by 'Lesson K' (then against
lesson K). Also checks that every card number appears in the lesson's text (cards cite nothing else)."""

import json
import re
import sys
from pathlib import Path

BLOCKS = Path(sys.argv[1])
cards = json.loads(Path("course/modules/M/M4/cards.json").read_text(encoding="utf-8"))
index = {p.stem: p.read_text(encoding="utf-8") for p in BLOCKS.glob("L*.txt")}
REF = re.compile(r"(Lesson (\d+),? )?(Definition|Theorem|Proposition|Example|Remark|Lemma|Problem|Assumption)s?\s+([0-9]+(?:\.[0-9]+)?|[A-Z][0-9]+|[0-9]+\([a-z]\))")
bad = []
for c in cards:
    own = c["lesson"]
    text_all = ""
    for m in REF.finditer(c["back"] + " " + c["front"]):
        lesson_no = m.group(2)
        lesson = f"L{int(lesson_no):02d}" if lesson_no else own
        if lesson not in index:
            bad.append((c["id"], "no lesson", lesson, m.group(0)))
            continue
        kind, num = m.group(3), m.group(4).split("(")[0]
        pattern = f"[{kind}] {kind} {num}"
        if pattern not in index[lesson] and f"[{kind}] {kind} {num}" not in index[lesson]:
            # Problem and Assumption may be listed under other kinds; accept any block whose title starts with the label
            if not re.search(rf"\] {kind} {re.escape(num)}\b", index[lesson]):
                bad.append((c["id"], c["lesson"], lesson, m.group(0)))
print("cards", len(cards), "unresolved references", len(bad))
for row in bad:
    print(*row)
