"""For each M2 card, check that every locator it cites (Theorem/Proposition/Lemma/Corollary/Example/Remark/Assumption
x.y, Misconception n, Problem <id>, Section n, Lab 1 part X) exists in the card's own lesson text (round 2).

Usage: python3 -I card_locators.py <checkout> <clean-text-dir>
"""
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
clean = pathlib.Path(sys.argv[2])
cards = json.loads((root / "course/modules/M/M2/cards.json").read_text(encoding="utf-8"))
texts = {}
problems = []
checked = 0
PAT = re.compile(r"(Theorem|Proposition|Lemma|Corollary|Example|Remark|Assumption|Definition) (\d+\.\d+)")
for c in cards:
    lesson = c["lesson"]
    if lesson not in texts:
        texts[lesson] = (clean / f"{lesson}.txt").read_text(encoding="utf-8")
    t = texts[lesson]
    blob = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    for kind, num in PAT.findall(blob):
        checked += 1
        if not re.search(rf"{kind} {re.escape(num)}\b", t):
            problems.append((c["id"], f"{kind} {num}"))
    for m in re.findall(r"Misconception (\d)", blob):
        checked += 1
        if f"Misconception {m}" not in t and "“" not in t:
            problems.append((c["id"], f"Misconception {m}"))
        elif not re.search(rf"Misconception {m}", t):
            problems.append((c["id"], f"Misconception {m}"))
    for m in re.findall(r"Problem (L\d\d-[A-Z]\d|M\d|E\d|P\d|R\d)", blob):
        checked += 1
        if not re.search(rf"(?:Problem |{lesson}-|M2-{lesson}\s*·)" + re.escape(m) + r"|" + re.escape(m) + r"\b", t):
            problems.append((c["id"], f"Problem {m}"))
    for m in re.findall(r"Section (\d)", blob):
        checked += 1
        if not re.search(rf"^{m}[A-Z]", t, re.M) and not re.search(rf"^{m}\s", t, re.M):
            problems.append((c["id"], f"Section {m}"))
print("locators checked:", checked)
print("locators not found in the card's lesson text:", len(problems))
for p in problems:
    print("  ", p)
