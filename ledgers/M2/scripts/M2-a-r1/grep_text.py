"""Search the visible text of a course page for a regex and print each hit with context.

Usage: python -I grep_text.py <file.html> <regex> [width]
"""
import html
import re
import sys

fn, pat = sys.argv[1], sys.argv[2]
w = int(sys.argv[3]) if len(sys.argv) > 3 else 160
t = open(fn, encoding="utf-8").read()
t = re.sub(r"<script.*?</script>", "", t, flags=re.S)
t = re.sub(r"<[^>]+>", " ", t)
t = re.sub(r"\s+", " ", html.unescape(t))
for m in re.finditer(pat, t, flags=re.I):
    print(fn, "...", t[max(0, m.start() - w // 2): m.end() + w // 2])
    print()
