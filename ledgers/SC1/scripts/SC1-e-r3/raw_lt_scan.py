"""Scan lesson HTML for raw '<' characters that a browser parses as tag starts (read-only, stdlib only).

Usage: raw_lt_scan.py <page.html> [...]
Prints each '<' followed by a letter, with the tag-like name and the line number, when the name is not a
known HTML element. Such a '<' inside \\( ... \\) or text is a parse hazard.
"""
import re
import sys

KNOWN = set("""a abbr article aside audio b blockquote body br button canvas caption cite code col colgroup dd del
details dfn div dl dt em fieldset figcaption figure footer form h1 h2 h3 h4 h5 h6 head header hr html i iframe img input
ins kbd label legend li link main map mark math meta nav noscript object ol optgroup option p param pre q s samp script
section select small source span strong style sub summary sup svg table tbody td template textarea tfoot th thead time
title tr u ul var video wbr path g line rect circle text defs use annotation semantics mi mo mn msup mrow mfrac msub
mtext mtd mtr mtable munder mover mspace mstyle msqrt mroot mfenced mrow""".split())

for path in sys.argv[1:]:
    text = open(path, encoding="utf-8").read()
    hits = []
    for m in re.finditer(r"<([A-Za-z][A-Za-z0-9]*)", text):
        name = m.group(1).lower()
        if name not in KNOWN:
            line = text.count("\n", 0, m.start()) + 1
            hits.append((line, m.group(0)))
    print(f"{path}: {len(hits)} suspicious '<' tag starts")
    for line, tok in hits:
        print(f"  line {line}: {tok}")
