"""Check that the printed-output lines of each L-lab twin occur in its lesson page text (round 3).

Usage: python3 -I output_vs_page.py <repo-root> <labout-dir>
"""
import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
outdir = Path(sys.argv[2])
for n in range(1, 9):
    out = (outdir / f"L0{n}.out").read_text(encoding="utf-8")
    page = html.unescape(re.sub(r"<[^>]+>", " ", (root / f"course/modules/M/M7/L0{n}.html").read_text(encoding="utf-8")))
    page = " ".join(page.split())
    lines = [" ".join(ln.split()) for ln in out.splitlines() if ln.strip()]
    missing = [ln for ln in lines if ln not in page]
    print(f"L0{n} output lines {len(lines)} not verbatim in page text {len(missing)}")
    for ln in missing[:6]:
        print("   ", ln[:150])
