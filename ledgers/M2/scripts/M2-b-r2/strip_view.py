"""Print an HTML page as numbered text lines (tags stripped, source line numbers kept).

Only a '<' that starts a real tag (followed by a letter, '/' or '!') is removed, so literal '<' in math survives.
"""
import html
import re
import sys

path = sys.argv[1]
tag = re.compile(r"<(?=/?[A-Za-z!])[^>]*>")
with open(path, encoding="utf-8") as fh:
    for no, line in enumerate(fh, 1):
        text = html.unescape(tag.sub("", line)).strip()
        if text:
            print(f"{no}: {text}")
