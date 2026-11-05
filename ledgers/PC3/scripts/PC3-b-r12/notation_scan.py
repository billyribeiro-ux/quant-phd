"""Scan math spans of the PC3 L04-L06 pages: list every macro and every symbol token, with counts.

Stdlib only. Usage: python -I notation_scan.py <checkout_root>
"""
import collections
import html
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
for page in ("L04", "L05", "L06"):
    text = (root / f"course/modules/PC/PC3/{page}.html").read_text(encoding="utf-8")
    spans = re.findall(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", text, re.S)
    maths = [html.unescape(a or b) for a, b in spans]
    cmds = collections.Counter()
    letters = collections.Counter()
    for m in maths:
        m2 = re.sub(r"\\(text|operatorname|mathrm|mathbf|mathcal|mathbb)\{([^}]*)\}", r"\2", m)
        for c in re.findall(r"\\([A-Za-z]+)", m):
            cmds[c] += 1
        for c in re.findall(r"(?<![A-Za-z\\])([A-Za-z])(?![A-Za-z])", re.sub(r"\\[A-Za-z]+", " ", m2)):
            letters[c] += 1
        for c in re.findall(r"\\mathbb\{[^}]*\}", m):
            cmds["mathbb:" + c] += 1
    print(page, "math spans", len(maths))
    print("  commands", dict(sorted(cmds.items())))
    print("  single letters", dict(sorted(letters.items())))
