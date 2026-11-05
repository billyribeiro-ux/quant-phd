"""Check every curly-quoted passage of a lesson page against the primary statute text.

usage: python3 -I quotecheck_r10.py <page.html> <source.txt> [<source.txt> ...]
Prints OK when every piece (>= 4 words, split at brackets and ellipses) occurs in the flattened source.
"""
import html
import re
import sys


def norm(s: str) -> str:
    s = html.unescape(s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("—", "--"), ("–", "-"), ("­", "")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip()


def flat(paths: list[str]) -> str:
    t = ""
    for p in paths:
        raw = open(p, encoding="utf-8", errors="replace").read()
        raw = re.sub(r"(\w)-\n\s*(\w)", r"\1\2", raw)
        t += " " + raw
    t = norm(t)
    return re.sub(r"\s+", " ", t)


def main() -> None:
    page = open(sys.argv[1], encoding="utf-8").read()
    page = re.sub(r"<[^>]+>", "", page)
    src = flat(sys.argv[2:]).lower()
    src_nospace = re.sub(r"\s+", "", src)
    for q in re.findall(r"“([^”]{8,})”", page):
        qn = norm(q)
        pieces = [p.strip(" .,;:") for p in re.split(r"\[[^\]]*\]|\.\.\.|…", qn)]
        miss = [p for p in pieces if len(p.split()) >= 4 and p.lower() not in src]
        miss_ns = [p for p in pieces if len(p.split()) >= 4 and re.sub(r"\s+", "", p).lower() not in src_nospace]
        status = "OK  " if not miss else ("OKNS" if not miss_ns else "MISS")
        print(status, qn[:110], ("" if not miss else " || " + " ... ".join(m[:70] for m in miss)))


if __name__ == "__main__":
    main()
