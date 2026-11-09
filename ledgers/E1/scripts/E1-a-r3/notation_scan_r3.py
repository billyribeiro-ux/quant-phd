"""Notation scan for hub and L01-L03 (verifier r3): macros used vs notation.json, registered symbols in math, capital letters."""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
macros = set(reg["macros"])
symbols = [s["symbol"] for s in reg["symbols"]]
print("registered macros:", len(macros), "registered symbols:", symbols)
for page in ["index.html", "L01.html", "L02.html", "L03.html"]:
    src = (root / "course/modules/E/E1" / page).read_text(encoding="utf-8")
    math = " ".join(a or b for a, b in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", src, flags=re.S))
    used = set(re.findall(r"\\([A-Za-z]+)", math))
    custom = sorted(m for m in used if "\\" + m in macros)
    print(f"{page}: math spans use registered macros: {custom}")
    for sym in ["\\Phi", "\\gamma", "\\ast", "R_f", "\\mathbb", "T"]:
        hit = sym in math if sym != "T" else bool(re.search(r"(?<![A-Za-z\\])T(?![a-z])", math))
        if hit:
            print(f"  registered-symbol candidate in math: {sym}")
    caps = sorted(set(re.findall(r"(?<![\\A-Za-z])([A-Z])(?![a-z])", re.sub(r"\\[A-Za-z]+", "", math))))
    print(f"  capital letters used as variables: {caps}")
print("standard KaTeX commands used (non-macro):", sorted(set(re.findall(r"\\([A-Za-z]+)", " ".join(
    (root / 'course/modules/E/E1' / p).read_text(encoding='utf-8') for p in ['L01.html', 'L02.html', 'L03.html'])))))
