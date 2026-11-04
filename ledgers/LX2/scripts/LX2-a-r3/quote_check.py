"""Locate every double-quoted passage inside claim spans of a lesson page in an opinion's pdftotext output.

Usage: python3 -I quote_check.py <page.html> <opinion.txt> <cite-key> [<cite-key> ...]
Matching is on lowercase letters and digits only (punctuation, dash variants, quote variants, line breaks and
bracketed alterations are dropped on both sides). Running heads are removed. The printed page of a match is read
from the page's running head. Prints one line per quotation: status, printed page(s) found, locator, passage prefix.
"""

import bisect
import html
import re
import sys

PAGE_PATTERNS = [
    re.compile(r"Cite as: 521 U\. S\. 642 \(1997\)\s+(\d{3})"),
    re.compile(r"DIRKS v\. SEC\s+(\d{3})"),
    re.compile(r"^\s*(\d{3})\s+OCTOBER TERM", re.M),
]
HEAD = re.compile(r"Cite as:|Unit: \$U89|OCTOBER TERM|Opinion of the Court|DIRKS v\. SEC|UNITED STATES v\. O.HAGAN|PAGES PGT|^\s*\d{3}\s*$")


def alnum(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'")
    return re.sub(r"[^a-z0-9]", "", s.lower())


def build(text: str) -> tuple[str, list[tuple[int, int]]]:
    stream = []
    spans: list[tuple[int, int]] = []  # (start index in stream, printed page)
    pos = 0
    for page in text.split("\f"):
        m = None
        for pat in PAGE_PATTERNS:
            m = pat.search(page)
            if m:
                break
        printed = int(m.group(1)) if m else -1
        if printed == -1 and spans and spans[-1][1] > 0:
            # odd PDF pages of the U.S. Reports print no running number in the text: the page follows the last one
            printed = spans[-1][1] + 1
        kept = "\n".join(line for line in page.split("\n") if not HEAD.search(line))
        chunk = alnum(kept)
        spans.append((pos, printed))
        stream.append(chunk)
        pos += len(chunk)
    return "".join(stream), spans


def main() -> None:
    page_html, opinion_path = sys.argv[1], sys.argv[2]
    keys = sys.argv[3:]
    src = open(page_html, encoding="utf-8").read()
    text, spans = build(open(opinion_path, encoding="utf-8").read())
    starts = [s for s, _ in spans]
    claims = re.findall(r'<span class="claim"([^>]*)>(.*?)</span>', src, flags=re.S)
    n_total = n_found = 0
    for attrs, body in claims:
        cite = re.search(r'data-cite="([^"]*)"', attrs)
        loc = re.search(r'data-locator="([^"]*)"', attrs)
        if not cite or not any(k in cite.group(1).split() for k in keys):
            continue
        plain = html.unescape(re.sub(r"<[^>]+>", "", body))
        for q in re.findall(r"“(.*?)”", plain, flags=re.S):
            n_total += 1
            needle = alnum(re.sub(r"\[([^\]]*)\]", r"\1", q))
            hits = []
            idx = text.find(needle)
            while idx >= 0:
                hits.append(spans[bisect.bisect_right(starts, idx) - 1][1])
                idx = text.find(needle, idx + 1)
            if not hits:
                print(f"NOT FOUND | {loc.group(1) if loc else ''} | {q[:110]}")
                continue
            n_found += 1
            print(f"FOUND at printed pages {sorted(set(hits))} | {loc.group(1) if loc else ''} | {q[:70]}")
    print(f"quotations {n_total}, found {n_found}")


if __name__ == "__main__":
    main()
