"""Scan L13-L18 pages for registry-symbol macros and bare symbols (verifier round 3). Standard library only."""
import re, sys
paths = [f"course/modules/M/M2/L{n:02d}.html" for n in range(13, 19)]
registry_macros = [r"\E", r"\Prob", r"\Var", r"\Cov", r"\Corr", r"\N", r"\indic", r"\Normal", r"\iid", r"\dto", r"\pto", r"\argmax", r"\argmin", r"\tr", r"\diag", r"\SR", r"\hSR", r"\PSR"]
registry_symbols = ["\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}"]
for p in paths:
    txt = open(p, encoding="utf-8").read()
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", txt, flags=re.S)
    flat = " ".join(a or b for a, b in maths)
    hits = {m: flat.count(m) for m in registry_macros + registry_symbols if flat.count(m)}
    tbare = re.findall(r"(?<![A-Za-z\\])T(?![A-Za-z])", flat)
    print(p, "registry hits:", hits, "bare T in math:", len(tbare))
    syms = sorted(set(re.findall(r"(?<![A-Za-z\\])([A-Za-z])(?:_\{?[0-9a-z]+\}?)?(?![A-Za-z])", flat)))
    print("   single-letter symbols in math:", "".join(syms))
