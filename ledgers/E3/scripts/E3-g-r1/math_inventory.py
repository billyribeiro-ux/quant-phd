"""Round-18 verifier: inventory of math tokens per lesson page (L05-L08) and cards, for notation checks.
Prints each single-letter or named symbol inside \\( ... \\) and \\[ ... \\] with its count and the lines it occurs on."""
import html
import re
import sys
from collections import defaultdict
from pathlib import Path

root = Path(sys.argv[1])
pages = sys.argv[2:]
tok_re = re.compile(r"\\[A-Za-z]+|\b[A-Za-z]\b")
for page in pages:
    src = (root / f"course/modules/E/E3/{page}.html").read_text(encoding="utf-8")
    src = html.unescape(src)
    occ = defaultdict(list)
    for lineno, line in enumerate(src.split("\n"), 1):
        for m in re.finditer(r"\\\((.*?)\\\)|\\\[(.*?)\\\]", line, re.S):
            math = m.group(1) if m.group(1) is not None else m.group(2)
            for t in tok_re.findall(math):
                occ[t].append(lineno)
    print(f"== {page}")
    for t in sorted(occ, key=lambda x: (-len(occ[x]), x)):
        print(f"  {t!r} x{len(occ[t])} lines {sorted(set(occ[t]))[:12]}")
