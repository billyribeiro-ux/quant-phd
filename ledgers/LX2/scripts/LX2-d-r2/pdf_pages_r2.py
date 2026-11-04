"""Map phrases to PDF page numbers (pdftotext output, one PDF page per form-feed chunk).

Usage: python3 -I pdf_pages_r2.py <file.txt> <phrase> [<phrase> ...]
"""
import re
import sys

raw = open(sys.argv[1], encoding="utf-8", errors="replace").read()
chunks = raw.split("\f")


def norm(s: str) -> str:
    s = s.translate(str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-"}))
    s = re.sub(r"-\s*\n\s*", "", s)
    return re.sub(r"\s+", " ", s).lower()


for phrase in sys.argv[2:]:
    pages = [i + 1 for i, c in enumerate(chunks) if norm(phrase) in norm(c)]
    print(f"[{phrase}] pdf page(s): {pages if pages else 'NOT FOUND'}")
