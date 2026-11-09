"""LaTeX macro census over the M2 slice-c pages, with registry and standard-KaTeX classification (verifier scratch, round 1).

Run: .venv/bin/python -I ledgers/M2/scripts/M2-c-r1/macro_census.py [checkout-root]
"""
import collections
import json
import re
import sys

ROOT = sys.argv[1] if len(sys.argv) > 1 else "."
counts = collections.Counter()
for n in range(13, 19):
    text = open(f"{ROOT}/course/modules/M/M2/L{n}.html", encoding="utf-8").read()
    counts.update(re.findall(r"\\([A-Za-z]+)", text))
notation = json.load(open(f"{ROOT}/notation/notation.json", encoding="utf-8"))
registered_macros = {k.lstrip("\\") for k in notation["macros"]}
registered_symbols = [s["symbol"] for s in notation["symbols"]]
print("macros used (count):", sorted(counts.items(), key=lambda kv: -kv[1]))
print("registry macros used:", sorted(m for m in counts if m in registered_macros))
print("registry symbols:", registered_symbols)
for sym in registered_symbols:
    core = re.sub(r"[\\{}^_ ,()]", "", sym.split(",")[0])
    hits = 0
    for n in range(13, 19):
        text = open(f"{ROOT}/course/modules/M/M2/L{n}.html", encoding="utf-8").read()
        for math in re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S):
            body = math[0] or math[1]
            if core and re.search(r"(?<![A-Za-z])" + re.escape(core) + r"(?![A-Za-z])", body):
                hits += 1
    print(f"registry symbol {sym!r} (core {core!r}) appears in slice math: {hits}")
