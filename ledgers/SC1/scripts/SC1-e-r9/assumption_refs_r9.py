"""List every assumption label and 'of Lesson K' reference in the SC1 cards, and check the label is defined in the named lesson.

Usage: python -I assumption_refs_r9.py <repo_root> <out_dir>
"""
import json
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
out = pathlib.Path(sys.argv[2])
cards = json.loads((root / "course/modules/SC/SC1/cards.json").read_text(encoding="utf-8"))
txt = {f"L{n:02d}": (out / f"L{n:02d}.txt").read_text(encoding="utf-8") for n in range(1, 9)}
defined = {
    "L01": ["A1(a)", "A1(b)", "A1(c)", "A1(d)", "A1(e)"],
    "L02": ["Assumption 2.1", "Assumption A2", "A2"],
    "L03": ["Assumption 3.1", "Assumption 3.2"],
    "L04": ["Assumption 4.1", "Assumption 4.2", "4.2(b)", "4.2(c)", "4.2(d)"],
    "L05": ["A4(a)", "A4(b)", "A4(c)", "A4(d)", "A4(e)", "A4(f)", "A4(g)", "A4(h)", "A4(i)", "A3"],
    "L07": ["A5"],
}
labels = {}
for c in cards:
    s = c["front"] + " " + c["back"] + " " + str(c.get("basis", ""))
    for m in re.finditer(r"(A\d(?:\([a-i]\))?|Assumptions? \d\.\d(?:\([a-d]\))?)", s):
        labels.setdefault(m.group(1), []).append(c["id"])
print("distinct labels used in cards:", sorted(labels))
for lab in sorted(labels):
    ids = sorted(set(labels[lab]))
    where = [k for k in txt if re.search(re.escape(lab) if not lab.startswith("Assumption") else re.escape(lab), txt[k])]
    print(lab, "cards:", len(ids), "lessons mentioning label:", where)
print("--- 'of Lesson K' references")
for c in cards:
    s = c["front"] + " " + c["back"] + " " + str(c.get("basis", ""))
    for m in re.finditer(r"([^.;,]{0,60})of Lesson (\d)", s):
        print(c["id"], "[", c["lesson"], "]", m.group(0)[-70:])
