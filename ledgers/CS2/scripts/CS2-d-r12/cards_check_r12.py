"""Structural and numeric checks on course/modules/CS/CS2/cards.json against the lesson HTML (run with python -I)."""
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1]) / "course/modules/CS/CS2"
cards = json.loads((root / "cards.json").read_text(encoding="utf-8"))
print("entries", len(cards))
ids = [c["id"] for c in cards]
print("unique ids", len(set(ids)) == len(ids), "id pattern ok", all(re.fullmatch(r"CS2-c\d{3}", i) for i in ids))
print("keys", Counter(tuple(sorted(c.keys())) for c in cards))
print("grades", Counter(c["grade"] for c in cards))
lessons = {f"L{n:02d}" for n in range(1, 12)}
bad_lesson = [c["id"] for c in cards if c["lesson"] not in lessons]
print("lesson exists", not bad_lesson, bad_lesson)
per = Counter(c["lesson"] for c in cards)
print("per lesson", dict(sorted(per.items())))
print("every lesson has a card", set(per) == lessons)
nonT_no_basis = [c["id"] for c in cards if c["grade"] != "T" and not (c.get("cite") or c.get("basis"))]
print("non-T without cite/basis", nonT_no_basis)
fronts = Counter(c["front"].strip().lower() for c in cards)
backs = Counter(c["back"].strip().lower() for c in cards)
print("dup fronts", [k[:60] for k, v in fronts.items() if v > 1])
print("dup backs", [k[:60] for k, v in backs.items() if v > 1])
# numbers on each card must be present verbatim in its lesson text
lesson_text = {}
for l in sorted(lessons):
    raw = (root / f"{l}.html").read_text(encoding="utf-8")
    raw = re.sub(r"<[^>]+>", " ", raw)
    lesson_text[l] = raw
absent = []
for c in cards:
    nums = set(re.findall(r"\d+(?:\.\d+)?", c["front"] + " " + c["back"]))
    for n in nums:
        if n not in lesson_text[c["lesson"]]:
            absent.append((c["id"], n))
print("numbers absent from own lesson", len(absent), absent[:40])
