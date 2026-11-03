"""Scan TeX math in the E3 slice for uses of notation/notation.json symbols (verifier E3-e round 2).

Usage: python -I ledgers/E3/scripts/E3-e-r2/registry_symbol_scan.py
Math is taken from \\( ... \\) and \\[ ... \\] spans. Each registered symbol pattern is reported with file:line.
"""

import re

ROOT = "/Users/billyribeiro/.fanout/wt/verifyD2-E3-e/"
FILES = [
    "course/modules/E/E3/project.html",
    "course/modules/E/E3/L02.html",
    "course/modules/E/E3/L03.html",
    "course/modules/E/E3/L06.html",
    "course/modules/E/E3/L07.html",
    "course/modules/E/E3/L08.html",
    "course/modules/E/E3/L01.html",
    "course/modules/E/E3/L04.html",
    "course/modules/E/E3/L05.html",
    "course/modules/E/E3/index.html",
]
PATTERNS = {
    "T (observations)": r"(?<![A-Za-z\\])T(?![A-Za-z])",
    "Phi": r"\\Phi",
    "gamma_3/gamma_4": r"\\gamma_\{?[34]",
    "R^ast / R^{e ast}": r"R\^\{?(\\ast|e\\ast)",
    "R_f": r"R_f",
    "Q (measure)": r"\\mathbb\{Q\}|(?<![A-Za-z\\])Q(?![A-Za-z])",
    "SR/PSR/DSR/PBO": r"\\(SR|hSR|PSR|DSR|PBO|FWER|FDR|FDP|se|tr|diag|indic|argmax|argmin|dto|pto|iid|Normal)\b",
    "emgamma": r"\\emgamma",
}
MATH = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
for rel in FILES:
    text = open(ROOT + rel, encoding="utf-8").read()
    for m in MATH.finditer(text):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        line_no = text.count("\n", 0, m.start()) + 1
        for label, pat in PATTERNS.items():
            if re.search(pat, body):
                snippet = " ".join(body.split())[:110]
                print(f"{label:20s} {rel}:{line_no}: {snippet}")
