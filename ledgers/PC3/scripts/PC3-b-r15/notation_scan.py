"""List every TeX symbol used in L04-L06 and the registered symbols; flags any registered symbol used in the slice.

Run: python3 -I notation_scan.py <checkout_root>
"""
import json
import re
import sys

root = sys.argv[1]
nt = json.load(open(f"{root}/notation/notation.json", encoding="utf-8"))
registered = [s.get("tex", "") for s in nt["symbols"]]
pages = {p: open(f"{root}/course/modules/PC/PC3/{p}.html", encoding="utf-8").read() for p in ("L04", "L05", "L06")}
for p, src in pages.items():
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", src, re.S)
    tokens = set()
    for a, b in maths:
        expr = a or b
        for tok in re.findall(r"\\[A-Za-z]+|[A-Za-z](?:_\{?[A-Za-z0-9*]+\}?)?|\^\{?\\?ast\}?", expr):
            tokens.add(tok)
    print(p, "distinct math tokens:", sorted(tokens))
    for sym in registered:
        key = sym.split(",")[0].strip()
        if not key:
            continue
        core = key.replace("\\Phi", "").strip()
        if key in ("T", "\\Phi, \\Phi^{-1}", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}"):
            hits = [t for t in tokens if t.startswith(key.split("^")[0].split("_")[0].strip()[:2]) and key.strip("\\") in t]
    print(p, "registered symbol mentions:", [s for s in registered if s and any(s.split(",")[0].strip() in m for _, m in [(0, src)])][:3])
    print(p, "macros registered:", nt["macros"] if isinstance(nt["macros"], dict) else [m for m in nt["macros"]][:30])
