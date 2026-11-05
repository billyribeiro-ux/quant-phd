"""Locate every curly-quoted passage in LX2 slice-a pages in the printed source text, with its printed page.

Usage: python -I ledgers/LX2/scripts/LX2-a-r7/quote_locate.py <source_dir> <page.html> [<page.html> ...]

<source_dir> holds comps1884.txt, comps1885.txt, dirks.txt and ohagan.txt (pdftotext -layout output of the
GovInfo PDFs and the U.S. Reports PDFs, fetched by ledgers/LX2/scripts/LX2-a-r7/fetch_sources.sh).

For each quotation in a page (double curly quotes), prints the claim span it sits in (its data-cite and
data-locator, or NO-CLAIM), whether the text is FOUND in the named source, and the printed page(s) where it starts
(opinions: the page number printed in the running head of each form-feed page; statutes: the character offset).
Matching is case-, whitespace-, punctuation- and bracket-insensitive (only letters and digits are compared).
"""

import html
import os
import re
import sys

OPINION_FILES = {"dirks": "dirks.txt", "ohagan": "ohagan.txt"}
STATUTE_FILES = {"comps1884": "comps1884.txt", "comps1885": "comps1885.txt"}
HEAD_END = re.compile(r"\S\s{2,}(\d{3})\s*$")
HEAD_START = re.compile(r"^\s*(\d{3})\s{2,}\S")


def alnum(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"[^a-z0-9]", "", s.lower())


def printed_page(chunk: str) -> int | None:
    for line in chunk.split("\n"):
        if not line.strip():
            continue
        m = HEAD_START.match(line) or HEAD_END.search(line)
        if m:
            return int(m.group(1))
    return None


def load_opinion(path: str) -> list[tuple[int | None, str]]:
    with open(path, encoding="utf-8", errors="replace") as fh:
        chunks = fh.read().split("\f")
    return [(printed_page(c), alnum(c)) for c in chunks]


def load_statute(path: str) -> str:
    with open(path, encoding="utf-8", errors="replace") as fh:
        return alnum(fh.read())


def locate_opinion(pages: list[tuple[int | None, str]], q: str) -> str:
    hits = []
    for i, (pg, text) in enumerate(pages):
        at = text.find(q)
        if at >= 0:
            hits.append(f"p.{pg}")
    if hits:
        return "FOUND " + ",".join(hits)
    # Quotes that break across a page boundary: test each adjacent pair of pages.
    for i in range(len(pages) - 1):
        joined = pages[i][1] + pages[i + 1][1]
        at = joined.find(q)
        if at >= 0 and at < len(pages[i][1]) < at + len(q):
            return f"FOUND across p.{pages[i][0]}/p.{pages[i + 1][0]}"
    return "NOT FOUND"


def page_text(path: str) -> str:
    with open(path, encoding="utf-8") as fh:
        raw = fh.read()
    raw = re.sub(r"<[^>]+>", " ", raw)
    return html.unescape(raw)


CLAIM = re.compile(r'<span class="claim"([^>]*)>(.*?)</span>', re.S)
ATTR = re.compile(r'data-cite="([^"]*)"|data-locator="([^"]*)"')
QUOTE = re.compile(r"“([^”]+)”")


def claim_quotes(raw: str):
    """Yield (cite, locator, quote_text) for every double-curly quotation, with its enclosing claim span if any."""
    spans = []
    for m in CLAIM.finditer(raw):
        attrs = dict(re.findall(r'(data-[a-z]+)="([^"]*)"', m.group(1)))
        spans.append((m.start(), m.end(), attrs.get("data-cite", ""), attrs.get("data-locator", ""), m.group(2)))
    text = raw
    for qm in QUOTE.finditer(text):
        quote = re.sub(r"<[^>]+>", "", qm.group(1))
        cite, loc = "NO-CLAIM", ""
        for s, e, c, l, _ in spans:
            if s <= qm.start() < e:
                cite, loc = c, l
        yield cite, loc, html.unescape(quote)


def main() -> int:
    src = sys.argv[1]
    opinions = {k: load_opinion(os.path.join(src, v)) for k, v in OPINION_FILES.items()}
    statutes = {k: load_statute(os.path.join(src, v)) for k, v in STATUTE_FILES.items()}
    total = found = 0
    for page in sys.argv[2:]:
        with open(page, encoding="utf-8") as fh:
            raw = fh.read()
        print(f"== {page}")
        for cite, loc, quote in claim_quotes(raw):
            total += 1
            q = alnum(quote)
            if len(q) < 12:
                status = "SHORT (not checked)"
            else:
                status = None
                if "gpo1983dirks" in cite or "gpo1997united" in cite:
                    key = "dirks" if "gpo1983dirks" in cite else "ohagan"
                    if cite.count("gpo") == 2:
                        key = None
                    if key:
                        status = locate_opinion(opinions[key], q)
                    else:
                        status = "AMBIGUOUS key (checked in both)"
                        a = locate_opinion(opinions["dirks"], q)
                        b = locate_opinion(opinions["ohagan"], q)
                        status += f" dirks:{a} ohagan:{b}"
                if cite == "NO-CLAIM":
                    a = locate_opinion(opinions["dirks"], q)
                    b = locate_opinion(opinions["ohagan"], q)
                    hits = [k for k, t in statutes.items() if q in t]
                    status = f"NO-CLAIM dirks:{a} ohagan:{b} statute:{','.join(hits) or 'none'}"
                elif status is None or "gpondsecur" in cite:
                    hits = [k for k, t in statutes.items() if q in t]
                    if hits:
                        status = f"FOUND statute {','.join(hits)}"
                    elif status is None:
                        status = "NOT FOUND"
            if status.startswith("FOUND"):
                found += 1
            print(f"[{cite}] ({loc}) {status} :: {quote[:110]}")
    print(f"quotations: {total}, found: {found}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
