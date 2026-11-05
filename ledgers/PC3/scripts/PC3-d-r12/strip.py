"""Strip HTML tags from a lesson file, keeping source line numbers (for reading only)."""
import html
import re
import sys

src = sys.argv[1]
with open(src, encoding="utf-8") as fh:
    for n, line in enumerate(fh, 1):
        text = re.sub(r"<[^>]+>", "", line)
        text = html.unescape(text).strip()
        if text:
            print(f"{n:4d} {text}")
