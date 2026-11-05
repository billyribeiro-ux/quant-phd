r"""Find literal less-than characters inside math spans of SC1 lesson pages.

A literal '<' inside \(...\) or \[...\] is read by the HTML parser as a tag start when a letter follows it.
Usage: python -I raw_lt_check.py <paths...>. Prints file:line for each math span with a literal '<' and a
count per file. Greater-than is printed separately because a bare '>' is not parsed as a tag.
"""
import re
import sys

MATH = re.compile(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", re.S)
for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    lt = 0
    for m in MATH.finditer(text):
        body = m.group(1) if m.group(1) is not None else m.group(2)
        if "<" in body:
            lt += 1
            line = text.count("\n", 0, m.start()) + 1
            print(f"LT {path}:{line}: {body[:100]!r}")
    print(f"{path}: math spans with literal <: {lt}")
