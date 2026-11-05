"""Locate quoted phrases in the round-8 plain-curl opinion texts and report the printed U.S. Reports page.

Usage: python3 -I pagefind.py <opinion.txt> <phrase-file>
Every quotation mark, apostrophe and dash variant is matched as equal, and any run of whitespace (including a
hyphen at a line end) may stand between words. The printed page is the page number in the last page header
before the match. Header lines are recognised as: 'NNN OCTOBER TERM' / 'NNN UNITED STATES v. O'HAGAN' (even
pages), 'Cite as: 521 U. S. 642 (1997)  NNN' (odd O'Hagan pages) and 'DIRKS v. SEC  NNN' (odd Dirks pages).
Running heads such as 'NNN Opinion of the Court' are not headers. Every match is printed, because a phrase can
occur in the syllabus and in the opinion.
"""

import re
import sys

src, phrases_path = sys.argv[1], sys.argv[2]
raw = open(src, encoding="utf-8", errors="replace").read()

headers: list[tuple[int, int]] = []
pos = 0
for line in raw.split("\n"):
    s = line.replace("\f", " ").strip()
    m = None
    if len(s) < 110:
        m = re.match(r"^(\d{3})\s{2,}(OCTOBER TERM|UNITED STATES)", s)
        if m is None:
            m = re.search(r"(?:Cite as: 521 U\. S\. 642 \(1997\)|v\. SEC|DIRKS v\. SEC)\s+(\d{3})$", s)
    if m is not None and 640 <= int(m.group(1)) <= 700:
        headers.append((pos, int(m.group(1))))
    pos += len(line) + 1


def page_of(at: int) -> int | None:
    cur = None
    for hpos, num in headers:
        if hpos <= at:
            cur = num
        else:
            break
    return cur


QUOTES = "\"“”‘’'"
DASHES = "–—-"


def pattern(phrase: str) -> re.Pattern[str]:
    parts = []
    for ch in phrase:
        if ch in QUOTES:
            parts.append("[" + re.escape(QUOTES) + "]")
        elif ch in DASHES:
            parts.append("[" + re.escape(DASHES) + "]")
        elif ch.isspace():
            continue
        else:
            parts.append(re.escape(ch))
        parts.append(r"(?:\s+|-\s*\n\s*|\s*-\s*)?")
    return re.compile("".join(parts))


for phrase in open(phrases_path, encoding="utf-8").read().splitlines():
    phrase = phrase.strip()
    if not phrase:
        continue
    hits = list(pattern(phrase).finditer(raw))
    if not hits:
        print(f"NOT FOUND: {phrase}")
    for m in hits:
        print(f"FOUND page {page_of(m.start())} (match {m.start()}): {phrase}")
