"""Collect LaTeX commands and single-letter symbols from math spans in the BK4 slice pages (notation check)."""
import json
import re
import sys
from collections import Counter

pages = ["course/modules/BK/BK4/index.html", "course/modules/BK/BK4/L01.html",
         "course/modules/BK/BK4/L02.html", "course/modules/BK/BK4/L03.html"]
reg = json.load(open("notation/notation.json"))
macros = set(reg["macros"].keys())
cmds = Counter()
spans = 0
for p in pages:
    text = open(p, encoding="utf-8").read()
    for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        spans += 1
        for c in re.findall(r"\\[A-Za-z]+", body):
            cmds[c] += 1
print("math spans", spans)
print("commands", sorted(cmds.items()))
print("commands not in registry macros", sorted(c for c in cmds if c not in {"\\" + k.lstrip("\\") for k in macros}))
print("mathbb occurrences in pages", sum(open(p, encoding="utf-8").read().count("mathbb") for p in pages))
print("registered symbol hits (T, Phi, gamma_3, gamma_4, R^*, R_f, Q):")
for p in pages:
    text = open(p, encoding="utf-8").read()
    for m in re.finditer(r"\\\((.*?)\\\)", text, re.S):
        b = m.group(1)
        if re.search(r"(?<![A-Za-z])T(?![A-Za-z])|\\Phi|\\gamma|\\ast|R_f|\\mathbb\{Q\}|\bQ\b", b):
            print(p, b[:120])
