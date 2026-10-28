"""Check that every line printed by a real run of a slice twin appears verbatim in its lesson page.

Usage: python -I embed_match.py <page.html> <run_output.txt>
Prints MISSING lines and a count. The page text is html-unescaped first.
"""

from __future__ import annotations

import html
import re
import sys

page = html.unescape(open(sys.argv[1], encoding="utf-8").read())
page = re.sub(r"\s+", " ", page)
lines = [ln.rstrip() for ln in open(sys.argv[2], encoding="utf-8") if ln.strip()]
missing = [ln for ln in lines if re.sub(r"\s+", " ", ln.strip()) not in page]
print(f"{sys.argv[1].split('/')[-1]}: {len(lines) - len(missing)}/{len(lines)} output lines found verbatim")
for ln in missing:
    print("  MISSING:", ln)
