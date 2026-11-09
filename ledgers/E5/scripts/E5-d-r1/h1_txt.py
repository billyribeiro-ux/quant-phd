"""Dump a lesson/page as numbered plain text lines (tags stripped, entities unescaped). Usage: h1_txt.py FILE [PATTERN]"""
import html, re, sys
src = open(sys.argv[1], encoding="utf-8").read()
pat = re.compile(sys.argv[2]) if len(sys.argv) > 2 else None
for n, line in enumerate(src.split("\n"), 1):
    t = html.unescape(re.sub(r"<[^>]+>", "", line)).strip()
    if t and (pat is None or pat.search(t)):
        print(f"{n}: {t}")
