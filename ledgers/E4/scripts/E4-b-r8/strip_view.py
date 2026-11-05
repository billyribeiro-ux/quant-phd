"""Line-preserving text view of an E4 lesson page: HTML tags removed, line numbers kept.

Usage: strip_view.py <file>. Only real tags (an opening '<' followed by a letter, '/' or '!') are removed,
so a math '<' followed by a space, digit or backslash survives.
"""

import html
import re
import sys

path = sys.argv[1]
TAG = re.compile(r"</?[a-zA-Z!][^>]*>")
for n, line in enumerate(open(path, encoding="utf-8"), 1):
    t = html.unescape(TAG.sub("", line)).rstrip()
    if t.strip():
        print(f"{n}: {t}")
