"""Collect the math symbols used in LX2 lesson pages and compare them with notation/notation.json (run: python3 -I notation_scan.py <checkout>).

Prints every symbol token found in the math spans (\\( ... \\) and \\[ ... \\]) of L01-L04 and project.html, then the registered
symbols with their meaning, so a reader can check that no registered symbol is used with another meaning.
"""

import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
syms: set[str] = set()
for name in ("L01.html", "L02.html", "L03.html", "L04.html", "project.html"):
    s = (root / "course/modules/LX/LX2" / name).read_text(encoding="utf-8")
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", s, flags=re.S):
        body = m.group(1) or m.group(2)
        syms.update(re.findall(r"\\[A-Za-z]+|\b[A-Za-z](?:_\{?[A-Za-z0-9]+\}?)?", body))
print("symbols used in LX2 math:", sorted(syms))
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))["symbols"]
print("registered symbols:", [r["symbol"] for r in reg])
registered = {r["symbol"] for r in reg}
clash = sorted(t for t in syms if t in registered or any(t in r for r in registered if len(t) > 1))
print("LX2 tokens equal to a registered symbol:", clash)
