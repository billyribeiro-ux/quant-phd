"""Compare learner-visible text with raw '<' (as a browser parses it) and with '<' escaped inside math spans.
Prints each block whose visible text differs. Usage: raw_vs_escaped.py <page.html>"""
import difflib
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, ".")
from lesson_text import P, escape_math  # noqa: E402

src = open(sys.argv[1], encoding="utf-8").read()


def visible(text: str) -> str:
    p = P()
    p.feed(text)
    return re.sub(r"\n[ \t]*\n+", "\n", "".join(p.out))


raw = visible(src)
esc, n = escape_math(src)
fixed = visible(esc)
print("escaped count", n)
a = raw.split("\n")
b = fixed.split("\n")
for line in difflib.unified_diff(a, b, lineterm="", n=0):
    if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
        print(line[:400])
