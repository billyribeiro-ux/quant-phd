"""Strip tags from an HTML page, keeping line numbers: prints 'LINE: text' for each source line with tags removed."""
import re
import sys
import html

for n, line in enumerate(open(sys.argv[1], encoding="utf-8"), 1):
    t = re.sub(r"<[^>]+>", "", line)
    t = html.unescape(t).rstrip()
    if t.strip():
        print(f"{n}: {t}")
