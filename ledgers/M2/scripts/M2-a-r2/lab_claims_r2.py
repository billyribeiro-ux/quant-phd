"""Round-2 lab claim scan: sentences in each slice lab twin docstring that say the lab 'checks' something,
and what the code does with that quantity (comparison or print only). Run from the checkout root with -I.
"""

from __future__ import annotations

import ast
import re

for n in range(1, 7):
    path = f"tests/labs/M2/lab-M2-L0{n}-1.py"
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    doc = ast.get_docstring(tree) or ""
    sents = [s.strip() for s in re.split(r"(?<=[.])\s+", doc.replace("\n", " ")) if re.search(r"\bcheck", s)]
    print(f"L0{n}: docstring 'check' sentences:")
    for s in sents:
        print("   -", s)
    compares = sum(isinstance(node, ast.Compare) for node in ast.walk(tree))
    asserts = sum(isinstance(node, ast.Assert) for node in ast.walk(tree))
    prints = sum(isinstance(node, ast.Call) and getattr(node.func, "id", "") == "print" for node in ast.walk(tree))
    print(f"   code: Compare nodes={compares} assert={asserts} print calls={prints}")
    if n == 6:
        touch = [ln.strip() for ln in src.splitlines() if "Fraction(-1)" in ln or "Fraction(1))" in ln]
        print("   L06 lines that touch f(-1)/f(1):", touch)
