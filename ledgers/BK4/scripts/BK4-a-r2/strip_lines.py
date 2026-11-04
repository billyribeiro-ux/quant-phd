"""Print a course page as numbered plain text, one HTML line per output line, tags removed.

Usage: python3 -I ledgers/BK4/scripts/BK4-a-r2/strip_lines.py <page.html> [start end]
Used by the BK4-a round-2 verifier to read every line of a slice page.
"""

import html
import re
import sys

TAG = re.compile(r"</?[a-zA-Z][^>]*>")


def main() -> None:
    path = sys.argv[1]
    start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
    end = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
    with open(path, encoding="utf-8") as fh:
        for n, raw in enumerate(fh, start=1):
            if n < start or n > end:
                continue
            text = html.unescape(TAG.sub("", raw)).strip()
            if text:
                print(f"{n}: {text}")


if __name__ == "__main__":
    main()
