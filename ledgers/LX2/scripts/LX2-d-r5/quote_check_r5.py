"""LX2-d round 5: every double-quoted string in the lesson plain text (L01-L04) must occur in a fetched source text.

Usage: python3 -I quote_check_r5.py <lesson-text-dir> <source-dir>
Normalises curly quotes and dashes, then compares alphanumeric characters only (case-folded), so punctuation,
line breaks and hyphenation do not block a match. Prints NOT FOUND for every quote absent from all sources.
"""
import re
import sys
from pathlib import Path

LESSON_DIR = Path(sys.argv[1])
SRC = Path(sys.argv[2])
SOURCES = ["COMPS-1884.txt", "COMPS-1885.txt", "USREPORTS-463-646.txt", "USREPORTS-521-642.txt", "letter.txt",
           "att.txt", "cfa-standards-of-practice-iii-a.r5.txt", "cfa-standards-of-practice-vi-a.r5.txt",
           "cfa-standards-of-practice-vi-b.r5.txt"]


def fold(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    return re.sub(r"[^0-9a-z]", "", s.lower())


corpus = "".join(fold((SRC / name).read_text(encoding="utf-8", errors="replace")) for name in SOURCES)
total = 0
missing = 0
for page in ["L01", "L02", "L03", "L04"]:
    text = (LESSON_DIR / f"{page}.txt").read_text(encoding="utf-8")
    for m in re.finditer(r"“([^”]{4,})”", text):
        quote = m.group(1)
        total += 1
        ok = fold(quote) in corpus
        if not ok:
            missing += 1
            print(f"NOT FOUND {page}: {quote[:160]}")
print(f"quotes checked: {total}; not found in sources: {missing}")
