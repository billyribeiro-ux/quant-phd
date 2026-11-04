"""LX2-d round 6: report whether each phrase occurs in a source text (whitespace, hyphen-break and quote-insensitive).

Usage: python3 -I phrase_check_r6.py <source.txt> <phrases.txt>
Each line of phrases.txt is one phrase. Output: MATCH <pdf-page-index> or NOMATCH, per phrase.
Page index counts form feeds (pdftotext -layout emits one per page).
"""
import re
import sys


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace("­", "")
    s = re.sub(r"-\s*\n\s*", "", s)
    s = re.sub(r"\s+", "", s)
    return s.lower()


def main() -> None:
    src = open(sys.argv[1], encoding="utf-8", errors="replace").read()
    pages = src.split("\f")
    npages = [norm(p) for p in pages]
    for line in open(sys.argv[2], encoding="utf-8"):
        ph = line.rstrip("\n")
        if not ph.strip():
            continue
        n = norm(ph)
        hits = [i + 1 for i, p in enumerate(npages) if n in p]
        print(("MATCH pages=" + ",".join(map(str, hits))) if hits else "NOMATCH", "|", ph[:110])


if __name__ == "__main__":
    main()
