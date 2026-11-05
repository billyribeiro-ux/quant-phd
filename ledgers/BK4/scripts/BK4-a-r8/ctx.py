"""Print regex matches with a character window, one per line: ctx.py PATTERN FILE... (case-insensitive)."""
import re
import sys

pat = re.compile(sys.argv[1], re.I)
for path in sys.argv[2:]:
    text = open(path, encoding="utf-8").read()
    for m in pat.finditer(text):
        line = text.count("\n", 0, m.start()) + 1
        s = max(0, m.start() - 70)
        e = min(len(text), m.end() + 70)
        snippet = text[s:e].replace("\n", " ")
        print(f"{path}:{line}: ...{snippet}...")
