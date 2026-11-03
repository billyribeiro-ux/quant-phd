"""Check that every non-empty line of each L-lab twin occurs in its lesson page (HTML-unescaped), round 3.

Usage: python3 -I twin_vs_page.py <repo-root>
"""
import html
import sys
from pathlib import Path

root = Path(sys.argv[1])
for n in range(1, 9):
    twin = (root / f"tests/labs/M7/lab-M7-L0{n}-1.py").read_text(encoding="utf-8").splitlines()
    page = html.unescape((root / f"course/modules/M/M7/L0{n}.html").read_text(encoding="utf-8"))
    missing = [ln for ln in twin if ln.strip() and ln.strip() not in page]
    print(f"L0{n} twin lines {sum(1 for ln in twin if ln.strip())} missing from page {len(missing)}")
    for ln in missing[:5]:
        print("   ", ln[:140])
