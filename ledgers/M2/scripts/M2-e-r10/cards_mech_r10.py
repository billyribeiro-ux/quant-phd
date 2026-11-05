"""Mechanical card checks for M2: numbers in front/back appear in the lesson text; near-duplicate fronts; grade/basis."""
import difflib
import json
import pathlib
import re
import sys

cards = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
text_dir = pathlib.Path(sys.argv[2])
texts = {p.stem: p.read_text(encoding="utf-8") for p in text_dir.glob("L*.txt")}

NUM = re.compile(r"(?<![A-Za-z_])\d+(?:\.\d+)?(?![\d.]*[A-Za-z])")
problems = []
for c in cards:
    lesson = texts.get(c["lesson"])
    if lesson is None:
        problems.append((c["id"], "no lesson text"))
        continue
    for field in ("front", "back"):
        for num in NUM.findall(c[field]):
            # skip trivial integers 0,1,2 and common ordinals
            if num in ("0", "1", "2", "10", "3"):
                continue
            if num not in lesson:
                problems.append((c["id"], field, num))
print("cards", len(cards))
print("numbers not found verbatim in the lesson text (excluding 0,1,2,3,10):", len(problems))
for p in problems:
    print("  ", p)

fronts = [(c["id"], c["front"]) for c in cards]
pairs = []
for i in range(len(fronts)):
    for j in range(i + 1, len(fronts)):
        r = difflib.SequenceMatcher(None, fronts[i][1], fronts[j][1]).ratio()
        if r >= 0.75:
            pairs.append((round(r, 3), fronts[i], fronts[j]))
print("front pairs with similarity >= 0.75:", len(pairs))
for p in sorted(pairs, reverse=True):
    print("  ", p[0], p[1][0], "|", p[1][1][:110], "||", p[2][0], "|", p[2][1][:110])

gc = {}
for c in cards:
    g = c.get("grade")
    gc[g] = gc.get(g, 0) + 1
    if g in ("C",) and not c.get("basis"):
        print("grade C without basis:", c["id"])
    if g == "T" and c.get("basis"):
        print("grade T with basis (check):", c["id"], c["basis"])
    if g is None and c.get("basis"):
        print("basis without grade:", c["id"])
print("grades", gc)
