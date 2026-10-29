"""Extract visible text from a lesson page for line-by-line reading.

Strips script/style blocks and real tags only (a tag starts with a letter, '/' or '!'), so a
raw less-than sign in prose or math survives.
"""
import html, re, sys, pathlib
src = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
src = re.sub(r"<(script|style)\b.*?</\1>", "", src, flags=re.S)
src = re.sub(r"<(br|/p|/li|/h[1-6]|/tr|/div|/section|/pre|/figcaption)[^>]*>", "\n", src)
src = re.sub(r"<[a-zA-Z/!][^>]*>", "", src)
for line in html.unescape(src).splitlines():
    line = line.rstrip()
    if line.strip():
        print(line)
