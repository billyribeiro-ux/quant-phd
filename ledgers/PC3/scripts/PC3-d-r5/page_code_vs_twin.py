"""Compare each lesson's embedded lab code block with its lab twin, and each embedded output block with the twin's output.

Usage: python -I ledgers/PC3/scripts/PC3-d-r5/page_code_vs_twin.py <checkout> <twin_out_dir>
"""
import difflib
import html
import pathlib
import re
import sys

root = pathlib.Path(sys.argv[1])
outdir = pathlib.Path(sys.argv[2])
for n in range(1, 7):
    page = (root / "course/modules/PC/PC3" / f"L{n:02d}.html").read_text(encoding="utf-8")
    pres = re.findall(r"<pre[^>]*>(.*?)</pre>", page, flags=re.S)
    twin = (root / "tests/labs/PC3" / f"lab-PC3-L{n:02d}-1.py").read_text(encoding="utf-8")
    code_blocks = [html.unescape(re.sub(r"<[^>]+>", "", p)) for p in pres if "from __future__" in p or "def part_one" in p]
    if not code_blocks:
        print(f"L{n:02d}: no code block found")
        continue
    code = max(code_blocks, key=len).strip("\n")
    a = [l.rstrip() for l in twin.strip("\n").splitlines()]
    b = [l.rstrip() for l in code.splitlines()]
    diff = list(difflib.unified_diff(a, b, "twin", "page", lineterm=""))
    print(f"L{n:02d}: twin lines {len(a)}, page code lines {len(b)}, diff lines {len(diff)}")
    for line in diff[:40]:
        print("   ", line)
