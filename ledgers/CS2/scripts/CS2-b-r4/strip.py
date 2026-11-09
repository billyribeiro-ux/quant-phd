"""Print a page with HTML tags removed, keeping source line numbers.

Usage: python -I strip.py <file.html> [start] [end]
Grade and class markers are kept as tokens so that the reader sees them.
"""
import html
import re
import sys

path = sys.argv[1]
start = int(sys.argv[2]) if len(sys.argv) > 2 else 1
end = int(sys.argv[3]) if len(sys.argv) > 3 else 10**9
lines = open(path, encoding="utf-8").read().split("\n")
for i, raw in enumerate(lines, 1):
    if i < start or i > end:
        continue
    s = raw
    s = re.sub(r'<span class="grade" data-grade="([A-Z])">[A-Z]</span>', r"[G:\1]", s)
    s = re.sub(r"<(dfn|span|a|em|strong|code|p|li|td|tr|h[1-6]|section|div|ul|ol|table|tbody|thead|th|summary|details|label|legend|fieldset|sup|sub|button|i|b)\b[^>]*>", "", s)
    s = re.sub(r"</?[a-zA-Z][^>]*>", "", s)
    s = html.unescape(s).strip()
    if s:
        print(f"{i}: {s}")
