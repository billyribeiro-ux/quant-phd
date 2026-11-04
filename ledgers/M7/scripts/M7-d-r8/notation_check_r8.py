"""Notation check for the M7 project page and labs: every macro used, and every registered symbol used with a different meaning.

Usage: python -I notation_check_r8.py <repo-root>
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(reg["macros"])
files = [root / "course/modules/M/M7/project.html", *sorted((root / "course/modules/M/M7").glob("L0*.html")),
         *sorted((root / "tests/labs/M7").glob("*.py"))]
used: dict[str, set[str]] = {}
for f in files:
    text = f.read_text(encoding="utf-8")
    for cmd in re.findall(r"\\[A-Za-z]+", text):
        used.setdefault(cmd, set()).add(f.name)
registered_hits = {m: sorted(used[m]) for m in macros if m in used}
print("registered macros used:", registered_hits)
print("distinct commands used:", len(used))
print("commands used (sorted):", sorted(used))
for entry in reg["symbols"]:
    print("registered symbol:", entry["symbol"], "| module", entry["module"])
