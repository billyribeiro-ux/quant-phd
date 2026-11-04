"""LX2-d round 4: locate phrases in the fetched source texts and report the printed page of each hit.

Usage: python3 -I find_phrase_pages.py <src-dir> <file.txt> <phrase> [<phrase> ...]
pdftotext -layout output is split on form feeds (one chunk per PDF page). The printed page is the
first 3-digit number found on the first lines of the chunk (the running head), which is how the
USREPORTS and COMPS PDFs print their page numbers. Whitespace and hyphens are dropped (squeeze) before matching,
so line-end hyphenation does not block a match; curly quotes and dashes are normalised first.
Prints each matching chunk index and its printed page, and matches=N as the number of chunks that contain the phrase.
"""
import re
import sys
from pathlib import Path


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("−", "-")
    return " ".join(s.split())


def squeeze(s: str) -> str:
    """Drop spaces and hyphens so that line-end hyphenation and line breaks do not block a match."""
    return re.sub(r"[\s-]+", "", s)


def main() -> None:
    src = Path(sys.argv[1]) / sys.argv[2]
    chunks = src.read_text(encoding="utf-8", errors="replace").split("\f")
    head_re = re.compile(r"\b(\d{1,3})\b")
    for phrase in sys.argv[3:]:
        target = norm(phrase)
        hits = []
        for i, chunk in enumerate(chunks):
            body = norm(chunk)
            if squeeze(target) in squeeze(body):
                head_lines = [ln for ln in chunk.splitlines() if ln.strip()][:3]
                nums = [m for ln in head_lines for m in head_re.findall(ln)]
                printed = next((n for n in nums if len(n) == 3), None) or next(iter(nums), "?")
                hits.append((i + 1, printed))
        print(f"{phrase!r}: matches={len(hits)} pdf_page_printed_page={hits[:8]}")


if __name__ == "__main__":
    main()
