"""Normalise a pdftotext -layout file (join hyphenated line breaks, collapse spaces) and print every match with context.

Usage: python3 -I norm_grep.py <file.txt> <phrase> [<phrase> ...]
Prints the phrase, the match count, and 300 characters of context before and after the first match.
"""
import re
import sys

path = sys.argv[1]
with open(path, encoding="utf-8", errors="replace") as fh:
    raw = fh.read()
text = re.sub(r"-\s*\n\s*", "", raw)  # hyphenated line breaks
text = re.sub(r"\s+", " ", text)
for phrase in sys.argv[2:]:
    norm = re.sub(r"\s+", " ", phrase)
    hits = [m.start() for m in re.finditer(re.escape(norm), text)]
    print(f"[{phrase}] matches={len(hits)}")
    if hits:
        s = hits[0]
        print("   ..." + text[max(0, s - 300): s + len(norm) + 300] + "...")
