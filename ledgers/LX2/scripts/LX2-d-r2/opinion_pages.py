"""Map phrases in the U.S. Reports PDF text (pdftotext -layout) to the printed U.S. Reports page.

Each PDF page is one form-feed-separated chunk. The printed page is read from that chunk's running header
('NNN OCTOBER TERM', 'DIRKS v. SEC NNN', 'NNN UNITED STATES v. O'HAGAN', 'UNITED STATES v. O'HAGAN NNN', or 'Cite as: ... NNN').
Usage: python3 -I opinion_pages.py <file.txt> <phrase> [<phrase> ...]
Prints every printed page on which the whitespace-normalised phrase occurs (after joining hyphenated breaks).
"""
import re
import sys

HEADER = re.compile(
    r"^\s*(6\d\d)\s+OCTOBER TERM"
    r"|DIRKS v\. SEC\s+(6\d\d)\s*$"
    r"|^\s*(6\d\d)\s+UNITED STATES v\. O.HAGAN"
    r"|UNITED STATES v\. O.HAGAN\s+(6\d\d)\s*$"
    r"|^\s*Cite as: [^\n]*?\s(6\d\d)\s*$"
)

path = sys.argv[1]
with open(path, encoding="utf-8", errors="replace") as fh:
    chunks = fh.read().split("\f")

QUOTES = str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u2013": "-", "\u2014": "-"})
pages: list[tuple[str, int | None]] = []
current: int | None = None
for chunk in chunks:
    for line in chunk.split("\n"):
        m = HEADER.search(line)
        if m:
            current = int(next(g for g in m.groups() if g))
            break
    norm = chunk.translate(QUOTES)
    norm = re.sub(r"-\s*\n\s*", "", norm)
    norm = re.sub(r"\s+", " ", norm)
    pages.append((norm, current))

for phrase in sys.argv[2:]:
    norm_phrase = re.sub(r"\s+", " ", phrase.translate(QUOTES))
    found = sorted({p for text, p in pages if norm_phrase in text})
    print(f"[{phrase}] printed page(s): {found if found else 'NOT FOUND'}")
