"""Search every curly-quoted passage in the L01 and L02 pages against the fetched source texts.

Usage: python -I quote_search.py <scratch dir with comps1884.txt, comps1885.txt, dirks.txt, ohagan.txt> <page.html> [<page.html> ...]
Prints each quotation (HTML tags stripped), its page, and FOUND or MISS (normalised search: whitespace collapsed,
hyphenation at line breaks joined, curly quotes and bracketed alterations removed, footnote-free).
"""
import html
import os
import re
import sys

src_dir = sys.argv[1]
pages = sys.argv[2:]
texts = {}
for name in ("comps1884.txt", "comps1885.txt", "dirks.txt", "ohagan.txt"):
    with open(os.path.join(src_dir, name), encoding="utf-8", errors="replace") as fh:
        texts[name] = fh.read()


def norm(s: str) -> str:
    s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    s = s.replace("—", "-").replace("–", "-")
    s = re.sub(r"\[([a-zA-Z])\]", r"\1", s)  # bracketed alteration like [u]nder -> under
    s = re.sub(r"-\s*\n\s*", "", s)
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^A-Za-z0-9 ]", "", s)
    return s.lower().strip()


corpus = {k: norm(v) for k, v in texts.items()}
for page in pages:
    raw = open(page, encoding="utf-8").read()
    raw = re.sub(r"<[^>]+>", "", raw)
    raw = html.unescape(raw)
    quotes = re.findall(r"“([^”]{12,})”", raw)
    print(f"== {page}: {len(quotes)} quotations")
    for q in quotes:
        nq = norm(q)
        hit = [k for k, c in corpus.items() if nq and nq in c]
        status = "FOUND in " + ",".join(hit) if hit else "MISS"
        print(f"{status} | {q[:150]}")
