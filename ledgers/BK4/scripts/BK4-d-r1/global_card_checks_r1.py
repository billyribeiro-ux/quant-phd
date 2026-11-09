# BK4 slice d, round 1 (verifier F31): whole-deck checks on cards.json against L01-L05 text (labels and numbers).
import json
import re
import subprocess
import sys

ROOT = "/Users/billyribeiro/.fanout/wt/verifyF31-BK4-d"
L = {}
for n in ["L01", "L02", "L03", "L04", "L05"]:
    L[n] = subprocess.run([sys.executable, "-I", ROOT + "/ledgers/BK4/scripts/BK4-d-r1/strip.py",
                           ROOT + f"/course/modules/BK/BK4/{n}.html"], capture_output=True, text=True, check=True).stdout
cards = json.load(open(ROOT + "/course/modules/BK/BK4/cards.json", encoding="utf-8"))
numtok = re.compile(r"\d[\d,./]*\d|\d")
labels = re.compile(r"\b(Proposition|Example|Remark|Problem|Definition|Assumption|Corollary)\s+(\d\.\d|[A-Z]\d|[A-Z]\b|\d)")
miss_num = []
miss_lab = []
for c in cards:
    text = c["front"] + " " + c["back"] + " " + c.get("basis", "")
    lt = L[c["lesson"]]
    for m in numtok.finditer(text):
        t = m.group(0).rstrip(".,")
        if t not in lt and t not in ("0", "1", "2", "3", "4"):
            miss_num.append((c["id"], t))
    for m in labels.finditer(text):
        lab = m.group(0)
        if lab not in lt and lab.split()[-1] not in lt:
            # allow the label in any lesson of the unit
            if not any(lab in L[k] for k in L):
                miss_lab.append((c["id"], lab))
print("cards checked:", len(cards))
print("numbers not in own lesson (excluding 0-4):", miss_num)
print("label references not found in any BK4 lesson:", miss_lab)

# Project and grader are not cited by any card (front, back, basis, cite)
proj = re.compile(r"project|memo|rubric|clearing_house|grader|test_project|project\.html|lab-BK4-project", re.I)
hits = [c["id"] for c in cards if proj.search(json.dumps(c, ensure_ascii=False))]
print("cards citing project, memo, rubric, grader or clearing_house:", hits)
