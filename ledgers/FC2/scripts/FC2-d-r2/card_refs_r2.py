"""FC2-d round 2: every cross-reference on a card (Definition/Proposition/Theorem/... n.m, Problem X n) must occur
in the lesson it names (its own lesson unless the card says 'of Lesson N' or 'Lesson N'). Reads lesson text written
by card_check_r2.py into <scratch>.
Usage: .venv/bin/python -I ledgers/FC2/scripts/FC2-d-r2/card_refs_r2.py <checkout> <scratch>
"""

import json
import re
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
cards = json.loads((root / "course/modules/FC/FC2/cards.json").read_text(encoding="utf-8"))
lessons = {f"L{n:02d}": (scratch / f"L{n:02d}.txt").read_text(encoding="utf-8") for n in range(1, 9)}
pat = re.compile(
    r"\b(Definition|Proposition|Theorem|Remark|Example|Lemma|Corollary|Assumption|Problem|Section)\s+(A\d+′?|[A-Z]\d+|\d+(?:\.\d+)?)"
)
unresolved = []
for c in cards:
    text = c["front"] + " " + c["back"]
    own = c["lesson"]
    for kind, num in pat.findall(text):
        # a reference to another lesson is written 'Lesson N' near it; test own lesson, then all lessons
        needle = f"{kind} {num}"
        if needle in lessons[own]:
            continue
        hits = [k for k, t in lessons.items() if needle in t]
        if kind == "Problem" or kind == "Section":
            # problems and sections are checked against the lesson text as well
            pass
        if not hits:
            unresolved.append((c["id"], own, needle))
        elif own not in hits:
            unresolved.append((c["id"], own, needle + " (found only in " + ",".join(hits) + ")"))
for row in unresolved:
    print(*row)
print("unresolved references:", len(unresolved))
