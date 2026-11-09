"""Scan slice lesson pages (raw HTML) for math macros and symbols versus notation/notation.json.

Usage: python v3_notation_scan.py <repo_root>
Prints every backslash-macro used inside \\( \\) or \\[ \\] and every occurrence of a registered symbol.
"""
import json
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
reg = json.loads((root / "notation/notation.json").read_text(encoding="utf-8"))
registered_macros = set(reg["macros"].keys())
registered_symbols = [s["symbol"] for s in reg["symbols"]]
print("registered macros:", sorted(registered_macros))
print("registered symbols:", registered_symbols)
math_re = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
for L in ["07", "08", "09", "10", "11", "12"]:
    src = (root / f"course/modules/M/M2/L{L}.html").read_text(encoding="utf-8")
    macros: dict[str, int] = {}
    maths = [m.group(1) or m.group(2) or "" for m in math_re.finditer(src)]
    for body in maths:
        for mac in re.findall(r"\\[A-Za-z]+", body):
            macros[mac] = macros.get(mac, 0) + 1
    unreg = {k: v for k, v in macros.items() if k not in registered_macros}
    print(f"L{L}: math spans={len(maths)} macros used={sorted(macros)}")
    print(f"L{L}: non-registered KaTeX commands (standard LaTeX ok): {sorted(unreg)}")
    hits = []
    for sym in ["R_f", "R^\\ast", "R^{e\\ast}", "\\mathbb{Q}", "\\Phi", "\\gamma_3", "\\gamma_4", "\\SR", "\\hSR", "\\PSR"]:
        if sym in src:
            hits.append(sym)
    print(f"L{L}: registered symbols present in raw source: {hits}")
    tsym = [b for b in maths if re.search(r"(?<![A-Za-z\\])T(?![A-Za-z])", b)]
    print(f"L{L}: math spans containing a bare capital T: {len(tsym)}")
    for b in tsym[:5]:
        print("   ", b[:160])
