"""Find raw '<' followed by a letter inside lesson math (a browser reads '<a' as a tag start). Read-only.

Usage: raw_lt_math_scan.py <page.html> [...]. A hit is a '<' + letter whose tag text, up to the next '>',
contains a LaTeX delimiter (backslash-paren) or is followed by a backslash-paren before any space.
"""
import re
import sys

for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    hits = []
    for m in re.finditer(r"<(?=[A-Za-z])", text):
        window = text[m.start(): m.start() + 60]
        head = re.match(r"<([A-Za-z][^\s>]*)", window).group(1)
        if "\\" in head or "(" in head or ")" in head:
            line = text.count("\n", 0, m.start()) + 1
            hits.append((line, window[:40].replace("\n", " ")))
    print(f"{path}: {len(hits)} hazard(s)")
    for line, snippet in hits:
        print(f"  line {line}: {snippet}")
