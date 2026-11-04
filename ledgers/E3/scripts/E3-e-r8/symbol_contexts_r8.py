"""Round-8: first contexts of named TeX symbols on the E3 pages (run: .venv/bin/python -I <this file> sym1 sym2 ...)."""

import pathlib
import re
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-E3-e/course/modules/E/E3")

for sym in sys.argv[1:]:
    print("#####", sym)
    count = 0
    pattern = re.compile(r"\\" + re.escape(sym) + r"(?![A-Za-z])")
    for page in sorted(ROOT.glob("*.html")):
        src = page.read_text(encoding="utf-8")
        for m in pattern.finditer(src):
            count += 1
            if count <= 4:
                snippet = src[max(0, m.start() - 110): m.end() + 70].replace("\n", " ")
                print(f"  {page.name}: ...{snippet}...")
    print("  total", count)
