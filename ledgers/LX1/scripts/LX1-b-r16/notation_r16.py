"""LX1-b round 16: symbol-usage scan for K (L03 net worth), A and P (ruling 16), across LX1 pages, twins and cards.

Run: .venv/bin/python -I ledgers/LX1/scripts/LX1-b-r16/notation_r16.py <checkout>
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
LX = root / "course/modules/LX/LX1"
TW = root / "tests/labs/LX1"
K = re.compile(r"(?<![A-Za-z])K(_|\b)")
A_SUB = re.compile(r"(?<![A-Za-z])A_(\{?[0-9tm]|\\)")
P_SUB = re.compile(r"(?<![A-Za-z])P_(\{?[0-9t])")
files = sorted(LX.glob("*.html")) + sorted(TW.glob("*.py"))
for f in files:
    lines = f.read_text(encoding="utf-8").split("\n")
    k = [i for i, line in enumerate(lines, 1) if K.search(line)]
    a = [i for i, line in enumerate(lines, 1) if A_SUB.search(line)]
    p = [i for i, line in enumerate(lines, 1) if P_SUB.search(line)]
    rel = f.relative_to(root)
    print(f"{rel}: K lines {k[:6]}{'...' if len(k) > 6 else ''} (n={len(k)}); A_ subscript lines {a} ; P_ subscript lines {p[:12]}{'...' if len(p) > 12 else ''} (n={len(p)})")
cards = json.loads((LX / "cards.json").read_text(encoding="utf-8"))
for c in cards:
    s = c["front"] + " " + c["back"]
    if K.search(s) or A_SUB.search(s) or P_SUB.search(s):
        print(f"card {c['id']} ({c['lesson']}): K={bool(K.search(s))} A_={bool(A_SUB.search(s))} P_={bool(P_SUB.search(s))}")
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
print("notation.json has a K symbol:", '"K"' in json.dumps(reg) or "\\K" in json.dumps(reg))
