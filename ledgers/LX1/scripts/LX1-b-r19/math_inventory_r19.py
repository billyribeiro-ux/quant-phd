"""Inventory of TeX macros and symbols in LX1 slice-b pages (round 18).

Usage: python -I ledgers/LX1/scripts/LX1-b-r19/math_inventory_r18.py <html files...>
Prints, per file: every \\macro used inside \\( \\) and \\[ \\] spans (with count and first line),
and every math span containing a registered symbol token (T, Phi, gamma_3, gamma_4, R^\\ast, R^{e\\ast}, R_f, \\mathbb{Q}, \\E).
"""
import re
import sys
from collections import defaultdict

SPAN = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
MACRO = re.compile(r"\\([A-Za-z]+)")
REG = re.compile(r"(\\Phi|\\gamma_3|\\gamma_4|R\^\\ast|R\^\{e\\ast\}|R_f|\\mathbb\{Q\}|\\E\b|(?<![A-Za-z\\])T(?![A-Za-z]))")

for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    macros: dict[str, list] = defaultdict(list)
    regs: list = []
    for m in SPAN.finditer(text):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        line = text.count("\n", 0, m.start()) + 1
        for mac in MACRO.findall(body):
            macros[mac].append(line)
        for r in REG.findall(body):
            regs.append((line, r if isinstance(r, str) else r[0], body[:90]))
    print(f"== {path}")
    for mac in sorted(macros):
        print(f"  macro \\{mac}: count {len(macros[mac])} first line {macros[mac][0]}")
    for line, tok, body in regs:
        print(f"  REGISTERED-TOKEN line {line}: {tok!r} in span: {body}")
