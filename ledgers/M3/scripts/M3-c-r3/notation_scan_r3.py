"""List the math commands and single-letter symbols used in the L07-L09 math spans (round-3 verifier).

Run from the checkout root: python -I ledgers/M3/scripts/M3-c-r3/notation_scan_r3.py
"""
import collections
import html
import re

pages = ["L07", "L08", "L09"]
for p in pages:
    src = open(f"course/modules/M/M3/{p}.html", encoding="utf-8").read()
    maths = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", src, flags=re.S)
    text = html.unescape(" ".join(a or b for a, b in maths))
    cmds = collections.Counter(re.findall(r"\\[a-zA-Z]+", text))
    print(p, "math spans", len(maths))
    print("  commands:", dict(sorted(cmds.items())))
    print("  raw operatorname uses:", len(re.findall(r"\\operatorname", text)),
          " \\tr uses:", len(re.findall(r"\\tr(?![a-zA-Z])", text)),
          " \\diag uses:", len(re.findall(r"\\diag(?![a-zA-Z])", text)),
          " \\R uses:", len(re.findall(r"\\R(?![a-zA-Z])", text)))
    singles = collections.Counter(re.findall(r"(?<![\\a-zA-Z])([A-Za-z])(?![a-zA-Z])", re.sub(r"\\[a-zA-Z]+", " ", text)))
    print("  single-letter symbols:", dict(sorted(singles.items())))
