"""Find a raw '<' followed by a letter inside a \\( \\) or \\[ \\] math span of a lesson page; such an '<' opens an HTML tag
and the browser hides the text up to the next '>'. Usage: raw_lt.py <page.html>"""
import re
import sys

src = open(sys.argv[1], encoding="utf-8").read()
hits = 0
for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", src, flags=re.S):
    span = m.group(0)
    for t in re.finditer(r"<(?=[A-Za-z/!])", span):
        hits += 1
        line = src.count("\n", 0, m.start() + t.start()) + 1
        ctx = span[max(0, t.start() - 40): t.start() + 60].replace("\n", " ")
        print(f"line {line}: ...{ctx}...")
print("raw '<' followed by a letter inside math:", hits)
