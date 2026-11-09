"""Print an HTML file line by line with tags removed; line numbers are kept (locator = file:line).

Only real tags (an opening or closing tag starting with a letter, or a comment/doctype) are removed, so
text such as 's < t' is kept.
"""
import html
import re
import sys

TAG = re.compile(r"</?[a-zA-Z][^>]*>|<!--.*?-->|<!DOCTYPE[^>]*>", re.IGNORECASE)
for n, line in enumerate(open(sys.argv[1], encoding="utf-8"), start=1):
    text = html.unescape(TAG.sub("", line)).rstrip()
    if text.strip():
        print(f"{n}: {text}")
