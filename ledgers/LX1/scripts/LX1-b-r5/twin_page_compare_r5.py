"""Compare the L03 and L04 pages with their lab twins (verifier round 5, LX1 slice b).

Checks, for each lab: (1) the page's data-run code block equals the twin file (after rstrip, since the
page block has no final newline); (2) the page's expected block equals the twin's captured stdout line
for line (files produced by running the twin alone under python -I -W error).
Run with: python3 -I this_script.py <checkout>
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
pages = {
    "L03": ("course/modules/LX/LX1/L03.html", "tests/labs/LX1/lab-LX1-L03-1.py", "twin_L03.out"),
    "L04": ("course/modules/LX/LX1/L04.html", "tests/labs/LX1/lab-LX1-L04-1.py", "twin_L04.out"),
}
out_dir = root / "ledgers/LX1/scripts/LX1-b-r5"
ok = True
for lab, (page_rel, twin_rel, out_name) in pages.items():
    text = (root / page_rel).read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    twin = (root / twin_rel).read_text(encoding="utf-8")
    page_code = html.unescape(code.group(1))
    same_code = page_code.rstrip() == twin.rstrip()
    exp_lines = html.unescape(expected.group(1)).split("\n")
    out_lines = (out_dir / out_name).read_text(encoding="utf-8").rstrip("\n").split("\n")
    same_exp = exp_lines == out_lines
    print(f"{lab}: code==twin {same_code} (page {len(page_code)} chars, twin {len(twin)} chars); "
          f"expected lines {len(exp_lines)}, output lines {len(out_lines)}, equal {same_exp}")
    if not (same_code and same_exp):
        ok = False
        for i, (a, b) in enumerate(zip(exp_lines, out_lines)):
            if a != b:
                print("  first difference at line", i + 1, repr(a), repr(b))
                break
print("ALL EQUAL" if ok else "MISMATCH")
