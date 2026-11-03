"""Compare each lesson's expected-output block with the twin's printed output (verifier round 3, slice e).

Usage: python -I v3_expected_vs_output.py <out_dir>
Reads course/modules/M/M7/L0n.html and the captured twin outputs <out_dir>/lab-M7-L0n-1.out.
"""
import html
import re
import sys
from pathlib import Path

out_dir = Path(sys.argv[1])
for n in range(1, 9):
    page = Path(f"course/modules/M/M7/L{n:02d}.html").read_text(encoding="utf-8")
    blocks = re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
    expected = html.unescape(blocks[0]).strip("\n") if blocks else None
    actual = (out_dir / f"lab-M7-L{n:02d}-1.out").read_text(encoding="utf-8").strip("\n")
    status = "MATCH" if expected == actual else "DIFF"
    print(f"L{n:02d} expected_blocks={len(blocks)} {status}")
    if expected != actual:
        el, al = (expected or "").splitlines(), actual.splitlines()
        for i in range(max(len(el), len(al))):
            e = el[i] if i < len(el) else "<none>"
            a = al[i] if i < len(al) else "<none>"
            if e != a:
                print(f"  line {i + 1}: page={e!r} twin={a!r}")
