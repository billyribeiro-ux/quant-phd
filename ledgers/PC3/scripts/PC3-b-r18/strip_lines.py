"""Print an HTML file as 'LINE: text' with tags stripped, keeping source line numbers.

Usage: python -I strip_lines.py <file> [start] [end]
Only used by the verifier to read prose at a line locator; the source is never modified.
"""
import html
import re
import sys

path = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
end = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
with open(path, encoding="utf-8") as fh:
    for n, line in enumerate(fh, 1):
        if n < start or n > end:
            continue
        text = re.sub(r"<[^>]+>", "", line)
        text = html.unescape(text).strip()
        if text:
            print(f"{n}: {text}")
