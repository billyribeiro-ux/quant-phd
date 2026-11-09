"""Print an HTML file one line at a time with its 1-based line number, tags removed.

Usage: python -I -W error v3_strip.py <file.html> [start] [end]
Every input line yields exactly one output line, so line numbers match the file.
Markup-only lines print an empty text part. Entities are unescaped.
"""

import html
import re
import sys

TAG = re.compile(r"<(?:/?[A-Za-z!][^>]*)>")


def main() -> None:
    path = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
    with open(path, encoding="utf-8") as fh:
        for number, raw in enumerate(fh, start=1):
            if number < start or number > end:
                continue
            text = html.unescape(TAG.sub("", raw.rstrip("\n")))
            text = re.sub(r"\s+", " ", text).strip()
            print(f"{number}|{text}")


main()
