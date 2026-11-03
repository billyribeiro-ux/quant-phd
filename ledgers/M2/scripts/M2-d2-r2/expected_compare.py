"""Compare each slice page's expected block with the twin's stdout (run under the pinned CPython)."""
import re, sys, html
from pathlib import Path
root = Path(sys.argv[1])
scr = Path(sys.argv[2])
for L in ("L22", "L23", "L24"):
    page = (root / f"course/modules/M/M2/{L}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected = html.unescape(m.group(1))
    got = (scr / f"twin_{L}.stdout").read_text(encoding="utf-8")
    print(L, "expected==stdout:", expected.rstrip("\n") == got.rstrip("\n"), "lines", len(expected.splitlines()), len(got.splitlines()))
    if expected.rstrip("\n") != got.rstrip("\n"):
        for a, b in zip(expected.splitlines(), got.splitlines()):
            if a != b:
                print("  EXP:", a); print("  GOT:", b)
