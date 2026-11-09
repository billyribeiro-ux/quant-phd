"""Line-preserving text dump of a lesson page: strips tags, keeps source line numbers.

A tag is "<" followed by a letter, "/" or "!", up to the next ">". A bare "<" followed by a
space or a digit (as in the math "x_0 < x_1") is text and is kept.

Usage: python3 -I textdump.py <html> <out>
"""

import html
import re
import sys

src, dst = sys.argv[1], sys.argv[2]
tag = re.compile(r"</?[A-Za-z!][^>]*>")
with open(src, encoding="utf-8") as fh, open(dst, "w", encoding="utf-8") as out:
    for n, line in enumerate(fh, 1):
        text = html.unescape(tag.sub(" ", line)).strip()
        text = re.sub(r"[ \t]+", " ", text)
        if text:
            out.write(f"{n}: {text}\n")
