"""List every TeX macro and every bare-capital/greek token inside math in the slice pages (index, L01-L03).

Run: .venv/bin/python -I ledgers/SC1/scripts/SC1-a-r4/notation_scan.py
"""
import collections
import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4] / "course" / "modules" / "SC" / "SC1"
PAGES = ["index.html", "L01.html", "L02.html", "L03.html"]
MATH = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
REGISTERED = {"E", "Prob", "Var", "Cov", "Corr", "R", "N", "indic", "Normal", "iid", "dto", "pto", "argmax", "argmin",
              "tr", "diag", "se"}
for name in PAGES:
    raw = (ROOT / name).read_text(encoding="utf-8")
    macros: collections.Counter[str] = collections.Counter()
    tokens: collections.Counter[str] = collections.Counter()
    for m in MATH.finditer(raw):
        body = html.unescape(m.group(1) or m.group(2))
        for mac in re.findall(r"\\([A-Za-z]+)", body):
            macros[mac] += 1
        body2 = re.sub(r"\\[A-Za-z]+", " ", body)
        for tok in re.findall(r"(?<![A-Za-z])[A-Za-z](?![A-Za-z])", body2):
            tokens[tok] += 1
    print(f"== {name}")
    print("  macros:", dict(sorted(macros.items())))
    print("  single-letter tokens:", dict(sorted(tokens.items())))
