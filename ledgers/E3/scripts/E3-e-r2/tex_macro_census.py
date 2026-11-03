"""Census of TeX macros in the E3 slice pages, against notation/notation.json (verifier E3-e round 2).

Usage: python -I ledgers/E3/scripts/E3-e-r2/tex_macro_census.py
Prints each macro used in the slice with its count and the first file:line, and flags direct \\mathbb{X} uses
whose registered macro (\\E, \\Prob, \\R, \\N) exists.
"""

import json
import re
from collections import Counter, defaultdict

ROOT = "/Users/billyribeiro/.fanout/wt/verifyD2-E3-e/"
FILES = [
    "course/modules/E/E3/project.html",
    "course/modules/E/E3/L02.html",
    "course/modules/E/E3/L03.html",
    "course/modules/E/E3/L06.html",
    "course/modules/E/E3/L07.html",
    "course/modules/E/E3/L08.html",
    "course/modules/E/E3/index.html",
]
reg = json.load(open(ROOT + "notation/notation.json", encoding="utf-8"))
registered = set(reg["macros"].keys())
count: Counter[str] = Counter()
first: dict[str, str] = {}
for rel in FILES:
    for n, line in enumerate(open(ROOT + rel, encoding="utf-8"), 1):
        for m in re.finditer(r"\\[A-Za-z]+", line):
            name = m.group(0)
            count[name] += 1
            first.setdefault(name, f"{rel}:{n}")
for name, c in sorted(count.items(), key=lambda kv: -kv[1]):
    tag = "REGISTERED" if name in registered else ""
    print(f"{name:14s} {c:5d} {first[name]} {tag}")
print("registered macros in use:", sorted(n for n in count if n in registered))
bb = defaultdict(list)
for rel in FILES:
    for n, line in enumerate(open(ROOT + rel, encoding="utf-8"), 1):
        for m in re.finditer(r"\\mathbb\{[A-Za-z]\}", line):
            bb[m.group(0)].append(f"{rel}:{n}")
print("direct \\mathbb uses:", {k: v[:4] for k, v in bb.items()})
