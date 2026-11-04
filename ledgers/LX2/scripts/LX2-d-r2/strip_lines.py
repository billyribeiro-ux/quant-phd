"""Print each line of an HTML file as 'N: text' with tags removed, for line-locator reading.

Usage: python3 -I strip_lines.py <file.html> [start] [end]
"""
import html
import re
import sys

path = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
end = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
with open(path, encoding="utf-8") as fh:
    lines = fh.read().split("\n")
for n, line in enumerate(lines, 1):
    if n < start or n > end:
        continue
    t = re.sub(r"<[^>]+>", "", line)
    t = html.unescape(t).strip()
    if t:
        print(f"{n}: {t}")
