"""Print each line of a lesson HTML with tags removed, keeping the source line number."""
import html
import re
import sys

for n, line in enumerate(open(sys.argv[1], encoding="utf-8"), start=1):
    text = re.sub(r"<[^>]+>", "", line)
    text = html.unescape(text).strip()
    if text:
        print(f"{n}: {text}")
