"""For each card in cards.json: every cited numbered result (Definition/Lemma/Proposition/Theorem/Corollary/Result/Example/Remark/Problem/Part) and every number of 3+ digits or decimal in the answer must appear in the lesson text of the card's lesson (or in the cited lesson, if the card names one)."""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO = Path("/Users/billyribeiro/.fanout/wt/verifyC3-M6-d")
TEXT = REPO / "ledgers/M6/scripts/M6-d-r3/lesson_text"
cards = json.loads((REPO / "course/modules/M/M6/cards.json").read_text(encoding="utf-8"))
lessons = {p.stem: p.read_text(encoding="utf-8") for p in TEXT.glob("L*.txt")}
all_text = "\n".join(lessons.values())
ref_re = re.compile(r"\b(Definition|Lemma|Proposition|Theorem|Corollary|Result|Example|Remark|Problem|Assumption|Section|Part) ([A-Z]?\d+(\.\d+)?|[A-Z]\d*)\b")
num_re = re.compile(r"\b\d{3,}\b|\b\d+\.\d+\b")
problems = []
for card in cards:
    lesson = lessons.get(card["lesson"], "")
    body = card["front"] + " " + card["back"]
    refs = {m.group(0) for m in ref_re.finditer(body)}
    for r in sorted(refs):
        if r not in lesson:
            problems.append((card["id"], card["lesson"], "ref not in own lesson text", r, r in all_text))
    nums = {m.group(0) for m in num_re.finditer(body)}
    for n in sorted(nums):
        if n not in lesson:
            problems.append((card["id"], card["lesson"], "number not in own lesson text", n, n in all_text))
for p in problems:
    print(p)
print("total flagged", len(problems), "of", len(cards), "cards")
