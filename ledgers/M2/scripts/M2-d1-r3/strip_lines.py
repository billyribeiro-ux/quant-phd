"""Print an HTML lesson with source line numbers and tags removed (text only, math kept).

Only real tags (an opening '<' followed by a letter, '/' or '!') are removed, so a
literal '<' inside \\( ... \\) survives. Usage: python -I strip_lines.py <path-to-html>
"""
import html
import re
import sys

TAG = re.compile(r"</?[a-zA-Z!][^>]*>")

path = sys.argv[1]
with open(path, encoding="utf-8") as fh:
    for number, line in enumerate(fh, start=1):
        text = html.unescape(TAG.sub("", line)).rstrip()
        if text.strip():
            print(f"{number}: {text}")
