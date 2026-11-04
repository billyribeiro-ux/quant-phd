"""Map each curly-quoted passage of an LX2 page to the printed page of the opinion where it starts.

Usage: python -I page_map.py <dirks|ohagan> <source.txt> <page.html>
Printed page = the most recent page header above the match ("NNN UNITED STATES" / "NNN ... DIRKS" for even pages,
"Cite as ... NNN" for odd pages in O'Hagan; Dirks odd pages carry the number at the line end).
Matching is alphanumeric-only, case-insensitive, layout-independent. Quotes that do not match print NOTFND.
"""
import html
import re
import sys


def alnum(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    s = re.sub(r"\[([A-Za-z])\]", r"\1", s)
    return re.sub(r"[^a-z0-9]", "", s.lower())


def header_page(line: str, kind: str) -> int | None:
    if kind == "ohagan":
        m = re.search(r"Cite as: 521 U\. S\. 642 \(1997\)\s+(\d{3})\s*$", line)
        if m:
            return int(m.group(1))
        m = re.match(r"\s*(\d{3})\s+UNITED STATES v\. O", line)
        if m:
            return int(m.group(1))
    else:
        # odd pages: "DIRKS v. SEC NNN"; even pages: "NNN OCTOBER TERM, 1982". The running head
        # "NNN Opinion of the Court" (646) and "Opinion of the Court 463 U. S." are not page numbers.
        m = re.search(r"DIRKS v\. SEC\s+(\d{3})\s*$", line)
        if m:
            return int(m.group(1))
        m = re.match(r"\s*(\d{3})\s+OCTOBER TERM", line)
        if m:
            return int(m.group(1))
    return None


def main() -> int:
    kind, src, page = sys.argv[1], sys.argv[2], sys.argv[3]
    lines = open(src, encoding="utf-8", errors="replace").read().split("\n")
    # cumulative alnum text with a map from alnum index to line number and current page
    chars: list[str] = []
    char_line: list[int] = []
    line_page: list[int] = []
    cur = 0
    for i, ln in enumerate(lines):
        h = header_page(ln, kind)
        if h is not None:
            cur = h
        line_page.append(cur)
        for c in alnum(ln):
            chars.append(c)
            char_line.append(i)
    body = "".join(chars)
    raw = open(page, encoding="utf-8").read()
    text = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    quotes = re.findall(r"“([^”]{12,})”", text)
    for q in quotes:
        a = alnum(q)
        i = body.find(a)
        if i < 0:
            print(f"NOTFND {q[:90]}")
            continue
        ln = char_line[i]
        print(f"page {line_page[ln]:>4} line {ln + 1:>5}  {q[:90]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
