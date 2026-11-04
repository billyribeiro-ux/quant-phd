"""LX2-d round 1: label check against raw lesson markup (attributes included).

Section N is matched to <span class="section-number">N</span>; Problem X to the problem-title span 'X ·'.
Usage: .venv/bin/python ledgers/LX2/scripts/LX2-d-r1/cards_labels.py <checkout-root>
"""
import json, re, sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
UNIT = ROOT / "course/modules/LX/LX2"
cards = json.loads((UNIT / "cards.json").read_text(encoding="utf-8"))
raw = {p: (UNIT / f"{p}.html").read_text(encoding="utf-8").replace("&nbsp;", " ") for p in ["L01", "L02", "L03", "L04"]}
bad = 0
for c in cards:
    src = raw[c["lesson"]]
    text = c["front"] + " || " + c["back"] + " || " + c.get("basis", "")
    checks = []
    for m in re.finditer(r"\bSection (\d)\b", text):
        checks.append((m.group(0), re.search(rf'section-number">{m.group(1)}<', src) is not None))
    for m in re.finditer(r"\bProblem ([A-Z]\d)\b", text):
        checks.append((m.group(0), re.search(rf'>{m.group(1)} ·', src) is not None))
    for m in re.finditer(r"\bLab (\d)\b", text):
        checks.append((m.group(0), re.search(rf'Lab {m.group(1)} ·|Lab {m.group(1)}\b', src) is not None))
    for m in re.finditer(r"\b(Definition|Proposition|Theorem|Remark|Assumption|Example)\s+(\d\.\d|A\d)\b", text):
        label = m.group(0)
        checks.append((label, re.search(rf'{m.group(1)}\s+{re.escape(m.group(2))}\b', src) is not None))
    for m in re.finditer(r"\bpp?\. ?(\d+)(?:[–-](\d+))?(?: n\. (\d+))?", text):
        pg = m.group(1)
        if m.group(3):
            checks.append((m.group(0), re.search(rf"p\. ?{pg} n\. ?{m.group(3)}\b", src) is not None))
        else:
            checks.append((m.group(0), re.search(rf"pp?\. ?{pg}\b", src) is not None or re.search(rf"pp\. {pg}", src) is not None))
    for label, ok in checks:
        if not ok:
            bad += 1
            print(c["id"], "label not found in raw lesson markup:", label)
print("label checks failing:", bad)
