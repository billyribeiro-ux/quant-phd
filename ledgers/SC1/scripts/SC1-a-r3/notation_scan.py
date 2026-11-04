"""List every TeX macro and every bare-capital token used inside math delimiters in the SC1 L01-L03 and hub pages.

Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r3/notation_scan.py
"""

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path.cwd()
files = ["index.html", "L01.html", "L02.html", "L03.html"]
registered = set(json.loads((ROOT / "notation/notation.json").read_text())["macros"].keys())
macros = Counter()
letters = Counter()
for f in files:
    text = html.unescape((ROOT / "course/modules/SC/SC1" / f).read_text(encoding="utf-8"))
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S)
    for a, b in maths:
        s = a or b
        for mac in re.findall(r"\\[A-Za-z]+", s):
            macros[mac] += 1
        for tok in re.findall(r"(?<![\\A-Za-z])([A-Za-z])(?![A-Za-z])", re.sub(r"\\[A-Za-z]+", " ", s)):
            letters[tok] += 1
print("macros used (count):", dict(sorted(macros.items())))
print("registered macros used:", sorted(m for m in macros if m in registered))
print("unregistered macros used:", sorted(m for m in macros if m not in registered))
print("single letters inside math (count):", dict(sorted(letters.items())))
