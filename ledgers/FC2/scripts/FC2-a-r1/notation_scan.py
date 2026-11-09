"""Scan FC2 slice pages for macros and registered-symbol collisions (verifier, round 1).

Usage: python -I notation_scan.py <checkout-root>
Prints every backslash command used inside \\( \\) and \\[ \\] math, its count, and the
registered notation.json macros that it is compared against.
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

root = Path(sys.argv[1])
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
registered = set(reg["macros"].keys())
files = [root / f"course/modules/FC/FC2/{p}" for p in ("index.html", "L01.html", "L02.html", "L03.html")]
files.append(root / "course/modules/FC/FC2/cards.json")
math_re = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
cmd_re = re.compile(r"\\([A-Za-z]+)")
counts: Counter[str] = Counter()
per_file: dict[str, Counter[str]] = {}
for f in files:
    text = f.read_text(encoding="utf-8")
    if f.suffix == ".json":
        text = text.replace("\\\\", "\\")
    c: Counter[str] = Counter()
    for m in math_re.finditer(text):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        for cmd in cmd_re.findall(body):
            c["\\" + cmd] += 1
    per_file[f.name] = c
    counts.update(c)
print("registered macros:", sorted(registered))
for name, c in per_file.items():
    print(f"== {name}")
    for cmd, n in sorted(c.items()):
        flag = "REGISTERED" if cmd in registered else ""
        print(f"  {cmd:20s} {n:4d} {flag}")
