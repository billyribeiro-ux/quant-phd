"""Print an HTML page line by line as text, keeping raw line numbers.

Usage: textview.py <file.html>. Tags are removed; grade/cite/dfn markers are kept as [G:x] [C:keys] [DFN:id].
"""
import html
import re
import sys

path = sys.argv[1]
tag = re.compile(r"<[^>]+>")
for n, raw in enumerate(open(path, encoding="utf-8"), 1):
    marks = []
    for m in re.finditer(r'data-grade="([^"]*)"', raw):
        marks.append("G:" + m.group(1))
    for m in re.finditer(r'data-cite="([^"]*)"', raw):
        marks.append("C:" + m.group(1))
    for m in re.finditer(r'<dfn id="([^"]*)"', raw):
        marks.append("DFN:" + m.group(1))
    for m in re.finditer(r'data-locator="([^"]*)"', raw):
        marks.append("L:" + m.group(1))
    text = html.unescape(tag.sub("", raw)).strip()
    if not text and not marks:
        continue
    pre = (" [" + " ".join(marks) + "]") if marks else ""
    print(f"{n}:{pre} {text}")
