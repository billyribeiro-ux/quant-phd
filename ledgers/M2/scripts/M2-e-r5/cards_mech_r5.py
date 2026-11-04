"""Mechanical whole-set card checks for M2 (verifier round 5): ids, duplicates, grade fields, and labels cited by each card."""

import collections
import json
import pathlib
import re
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD5-M2-e/course/modules/M/M2")
cards = json.loads((ROOT / "cards.json").read_text(encoding="utf-8"))
ids = [c["id"] for c in cards]
print("cards", len(cards), "unique ids", len(set(ids)), "id format ok", all(re.fullmatch(r"M2-c\d{3}", i) for i in ids))
norm = lambda s: re.sub(r"\W+", " ", s.lower()).strip()
fronts = collections.Counter(norm(c["front"]) for c in cards)
print("duplicate fronts", [k for k, v in fronts.items() if v > 1])
print("per lesson", sorted(collections.Counter(c["lesson"] for c in cards).items()))
bad_grade = [c["id"] for c in cards if c.get("grade") not in (None, "T", "C")]
print("bad grade values", bad_grade)
grade_c_without_basis = [c["id"] for c in cards if c.get("grade") == "C" and not c.get("basis")]
print("grade C without basis", grade_c_without_basis)
grade_t_with_basis = [c["id"] for c in cards if c.get("grade") == "T" and c.get("basis")]
print("grade T with basis", grade_t_with_basis)
label_re = re.compile(r"\b(Proposition|Lemma|Theorem|Corollary|Definition|Example|Remark|Assumption|Misconception|Problem)\s+(\d+\.\d+|\d+|[A-Z]\d+)\b")
missing = []
for c in cards:
    text = c["front"] + " " + c["back"]
    lesson_text = (ROOT / f"{c['lesson']}.html").read_text(encoding="utf-8")
    plain = re.sub(r"<[^>]+>", " ", lesson_text)
    for m in label_re.finditer(text):
        kind, num = m.group(1), m.group(2)
        if kind == "Problem" and num[0] in "MERP" and num[1:].isdigit():
            continue  # problem labels are checked by reading the problem set
        if re.search(rf"\b{kind}\s+{re.escape(num)}\b", plain) is None:
            missing.append((c["id"], c["lesson"], f"{kind} {num}"))
print("label citations not found in own lesson (ignoring cross-lesson 'of Lesson'):", len(missing))
for row in missing[:40]:
    print("  ", row)
