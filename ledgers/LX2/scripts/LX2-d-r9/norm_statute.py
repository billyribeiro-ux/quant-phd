"""Normalise a pdftotext -layout dump of a U.S. Code compilation for phrase search.

Usage: python3 -I norm_statute.py <in.txt> <out.txt>
Drops the running page headers and the line-end hyphenation of the GovInfo layout, and joins each
paragraph onto one line so that a quoted phrase can be grepped across the printed line breaks.
"""

import re
import sys

src, dst = sys.argv[1], sys.argv[2]
text = open(src, encoding="utf-8", errors="replace").read()
lines = []
for raw in text.splitlines():
    s = raw.strip()
    if not s:
        lines.append("")
        continue
    if s.startswith("VerDate") or s.startswith("G:\\COMP") or re.match(r"^\d+\s+SECURITIES", s) or re.search(r"Sec\. \d+[A-Z]?$", s):
        continue
    lines.append(s)
joined = " ".join(lines)
joined = re.sub(r"(\w)- (\w)", r"\1\2", joined)
joined = re.sub(r"\s+", " ", joined)
open(dst, "w", encoding="utf-8").write(joined)
print("chars", len(joined))
