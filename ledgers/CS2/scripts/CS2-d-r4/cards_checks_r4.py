"""Verifier CS2-d round 4: automated checks on course/modules/CS/CS2/cards.json against the current lesson text.

Usage: python -I cards_checks_r4.py <checkout> <lesson-text-dir> <previous-cards.json>
Lesson text dir holds L01.txt..L11.txt, the plain text of each lesson page (extracted by the verifier from the checkout).
Checks: field set and grade rule (T has no basis; C has a basis that names a lab); every number in a back appears in its
own lesson text; every Definition/Proposition/Lemma/Theorem/Corollary/Remark/Assumption/Problem locator in a back appears
in its own lesson; no duplicate fronts or backs; cards added or changed since the previous pin.
"""

import glob
import json
import re
import sys
from collections import Counter
from pathlib import Path

checkout, lesson_dir, prev_path = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
cards = json.loads((checkout / "course/modules/CS/CS2/cards.json").read_text(encoding="utf-8"))
prev = {c["id"]: c for c in json.loads(prev_path.read_text(encoding="utf-8"))}
lessons = {Path(f).name[:3]: Path(f).read_text(encoding="utf-8") for f in glob.glob(f"{lesson_dir}/L*.txt")}

print("cards", len(cards), "grades", dict(Counter(c["grade"] for c in cards)))
fields = Counter(tuple(sorted(c)) for c in cards)
print("field sets", {k: v for k, v in fields.items()})
print("T with basis", [c["id"] for c in cards if c["grade"] == "T" and c.get("basis")])
print("C without basis", [c["id"] for c in cards if c["grade"] == "C" and not c.get("basis")])
print("C basis without a lab name", [c["id"] for c in cards if c["grade"] == "C" and "Lab" not in c.get("basis", "")])

missing_numbers = []
for c in cards:
    text = lessons[c["lesson"]]
    for tok in set(re.findall(r"\d[\d,.]*\d|\d", c["back"])):
        if tok.rstrip(".,") not in text and tok.replace(",", "") not in text:
            missing_numbers.append((c["id"], tok))
print("numbers in a back absent from its lesson", missing_numbers)

bad_locators = []
for c in cards:
    for kind, num in re.findall(r"\b(Definition|Proposition|Lemma|Theorem|Corollary|Remark|Assumption|Problem|Example)\s+(\d+\.\d+)", c["back"]):
        if f"{kind} {num}" not in lessons[c["lesson"]]:
            bad_locators.append((c["id"], f"{kind} {num}"))
print("locators absent from own lesson", bad_locators)

print("duplicate fronts", [k for k, v in Counter(c["front"].strip().lower() for c in cards).items() if v > 1])
print("duplicate backs", [k for k, v in Counter(c["back"].strip().lower() for c in cards).items() if v > 1])

added = [c["id"] for c in cards if c["id"] not in prev]
changed = [c["id"] for c in cards if c["id"] in prev and prev[c["id"]] != c]
unchanged = [c["id"] for c in cards if c["id"] in prev and prev[c["id"]] == c]
print("added", added)
print("changed", len(changed), changed)
print("unchanged", len(unchanged))
