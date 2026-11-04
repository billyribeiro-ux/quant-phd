"""Find every curly-quoted passage in the LX2 slice-a pages in the printed source text.

Usage: python -I quote_check.py <source_dir> <page.html> [<page.html> ...]
Each source file is read as text (pdftotext -layout output). Matching is case-insensitive
and whitespace-insensitive; square-bracket alterations such as [T]he are matched with the bracket removed.
Prints FOUND / NOT FOUND per quotation, with the source file and character offset for FOUND.
"""
import html
import os
import re
import sys

SOURCES = {
    "comps1884": "comps1884.txt",
    "comps1885": "comps1885.txt",
    "dirks": "dirks.txt",
    "ohagan": "ohagan.txt",
}


def alnum(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", norm(s))


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = s.replace("–", "-").replace("—", "-").replace(" ", " ")
    s = re.sub(r"\[([A-Za-z])\]", r"\1", s)
    s = s.replace("[", "").replace("]", "")
    s = re.sub(r"\s+", " ", s)
    return s.lower().strip()


def load(src_dir: str) -> dict[str, str]:
    out = {}
    for name, fn in SOURCES.items():
        with open(os.path.join(src_dir, fn), encoding="utf-8", errors="replace") as fh:
            out[name] = alnum(fh.read())
    return out


def page_text(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    raw = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(raw)


def main() -> int:
    src_dir = sys.argv[1]
    sources = load(src_dir)
    total = found = 0
    for page in sys.argv[2:]:
        text = page_text(page)
        quotes = re.findall(r"“([^”]{12,})”", text)
        print(f"== {os.path.basename(page)}: {len(quotes)} curly-quoted passages")
        for q in quotes:
            total += 1
            nq = alnum(q)
            # full quote, alphanumerics only (layout-independent); no ellipsis-splitting
            hit = None
            for name, body in sources.items():
                i = body.find(nq)
                if i >= 0:
                    hit = (name, i)
                    break
            if hit:
                found += 1
                print(f"FOUND  [{hit[0]}@{hit[1]}] {q[:110]}")
            else:
                print(f"NOTFND {q[:200]}")
    print(f"TOTAL {total} FOUND {found} NOTFOUND {total - found}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
