"""Scan the slice's math spans for registered notation (notation/notation.json) and list local symbols.

Usage: python3 -I notation_scan.py <repo-root>
Prints every math span that contains a registered symbol or macro, and the set of single-letter symbols used.
"""

import html
import json
import re
import sys

root = sys.argv[1]
reg = json.load(open(f"{root}/notation/notation.json", encoding="utf-8"))
macros = sorted(reg["macros"].keys(), key=len, reverse=True)
registered = ["\\Phi", "\\gamma_3", "\\gamma_4", "R^\\ast", "R^{e\\ast}", "R_f", "\\mathbb{Q}", "\\Phi^{-1}"]
pages = ["index", "L01", "L02", "L03", "L04"]
math = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
letters: dict[str, int] = {}
hits = []
for p in pages:
    text = open(f"{root}/course/modules/CS/CS2/{p}.html", encoding="utf-8").read()
    for m in math.finditer(text):
        span = html.unescape(m.group(1) or m.group(2) or "")
        line = text[: m.start()].count("\n") + 1
        for sym in registered + macros:
            if sym in span:
                hits.append((p, line, sym, span[:120]))
        for tok in re.findall(r"(?<![\\A-Za-z])([A-Za-z])(?![A-Za-z])", re.sub(r"\\[A-Za-z]+", " ", span)):
            letters[tok] = letters.get(tok, 0) + 1
for h in hits:
    print("HIT", *h)
print("LETTERS", dict(sorted(letters.items())))
print("registered symbols checked:", registered, "macros checked:", len(macros))
