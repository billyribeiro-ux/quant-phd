"""Check every curly-quoted passage in LX2 lesson pages and cards against the opinion text.

Usage: python3 -I quote_check.py <scratch/src dir> <checkout>
Reads the plain-curl PDF text (pdftotext output, page-split on form feed) of Dirks (USREPORTS-463-646)
and O'Hagan (USREPORTS-521-642), maps each PDF page to its printed page (Dirks 646+index; O'Hagan 642+index),
and reports for each quoted passage whether it occurs (letters and digits only, case-folded) and on which printed page.
"""

import html
import json
import re
import sys
from pathlib import Path

src = Path(sys.argv[1])
checkout = Path(sys.argv[2])


def norm(s: str) -> str:
    s = s.replace("’", "'").replace("‘", "'")
    return re.sub(r"[^a-z0-9]", "", s.lower())


def load(fn: str, base: int):
    raw = (src / fn).read_text(encoding="utf-8", errors="replace")
    pages = raw.split("\f")
    parts, spans = [], []
    pos = 0
    for i, p in enumerate(pages):
        # drop running headers (case name, term line, printed page numbers and the Westlaw/GovInfo header)
        keep = []
        for line in p.splitlines():
            s = line.strip()
            if re.fullmatch(
                r"(DIRKS v\. SEC|OCTOBER TERM, 1982|Opinion of the Court|521US2|Unit: \$U89.*|\[11-20-99.*|6[4-9]\d|\d{1,2})",
                s,
            ):
                continue
            keep.append(line)
        n = norm(" ".join(keep))
        spans.append((pos, pos + len(n), base + i))
        parts.append(n)
        pos += len(n)
    return "".join(parts), spans


TEXT = {
    "gpo1983dirks": load("dirks.txt", 646),
    "gpo1997united": load("ohagan.txt", 642),
}


def locate(key: str, quote: str):
    """Printed pages of every occurrence of the quote (a quote may recur, e.g. in the syllabus)."""
    text, spans = TEXT[key]
    q = norm(quote)
    if len(q) < 12:
        return None
    pages = []
    start = 0
    while True:
        idx = text.find(q, start)
        if idx < 0:
            break
        pages.append(sorted({pg for (a, b, pg) in spans if a <= idx < b}))
        start = idx + 1
    return pages or "NOT FOUND"


def quotes_in(s: str):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    return [m.strip() for m in re.findall(r"“(.+?)”", s, flags=re.S)]


if __name__ == "__main__":
    lesson_dir = checkout / "course/modules/LX/LX2"
    report = []
    for page in ("L02.html",):
        body = (lesson_dir / page).read_text(encoding="utf-8")
        for block in re.findall(r'data-cite="([^"]+)"[^>]*>(.*?)</span>', body, flags=re.S):
            cite, inner = block
            keys = [k for k in cite.split() if k in TEXT]
            if not keys:
                continue
            for qt in quotes_in(inner):
                res = {k: locate(k, qt) for k in keys}
                report.append((page, keys, qt[:110], res))
    cards = json.loads((lesson_dir / "cards.json").read_text(encoding="utf-8"))
    for c in cards:
        if c.get("lesson") != "L02":
            continue
        keys = [k for k in c.get("cite", []) if k in TEXT]
        for field in ("front", "back"):
            for qt in quotes_in(c.get(field, "")):
                res = {k: locate(k, qt) for k in (keys or ["gpo1983dirks", "gpo1997united"])}
                report.append((c["id"], keys, qt[:110], res))
    for r in report:
        print(r[0], r[1], repr(r[2]), r[3])
    print("total quotes", len(report))
