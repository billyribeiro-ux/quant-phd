"""Render an HTML page as text, one output line per source line, keeping source line numbers.

Usage: python -I html_lines.py <file.html> [start end]
Only real tags are stripped, so a bare '<' inside math such as '2 < S' is kept.
Used by the E4-b round-10 verifier to read slices line by line.
"""

import html
import re
import sys

TAG = re.compile(r"</?[a-zA-Z][a-zA-Z0-9]*(\s[^>]*)?/?>")

path = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
end = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
with open(path, encoding="utf-8") as fh:
    lines = fh.read().split("\n")
for no, line in enumerate(lines, 1):
    if no < start or no > end:
        continue
    text = TAG.sub("", line)
    text = html.unescape(text).strip()
    if text:
        print(f"{no}: {text}")
