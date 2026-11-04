"""Round-5 check for E4 slice a: each lab section's code and expected block versus its twin and its twin's output.

Usage: python -I check_twins_embed.py <checkout-root> <outdir-with-twin-outputs>
Reads only repository files and the twin-run stdout files written by the verifier.
"""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

root = Path(sys.argv[1])
outdir = Path(sys.argv[2])
page_dir = root / "course" / "modules" / "E" / "E4"
twin_dir = root / "tests" / "labs" / "E4"

ok = True
for lid in ("L01", "L02", "L03"):
    page = (page_dir / f"{lid}.html").read_text(encoding="utf-8")
    m = re.search(r'<section class="lab" id="(lab-E4-%s-1)"[^>]*>(.*?)</section>' % lid, page, re.S)
    if not m:
        print(lid, "no lab section")
        ok = False
        continue
    body = m.group(2)
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin = (twin_dir / f"lab-E4-{lid}-1.py").read_text(encoding="utf-8")
    out = (outdir / f"twin-{lid}.out").read_text(encoding="utf-8")
    err = (outdir / f"twin-{lid}.err").read_text(encoding="utf-8")
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    exp_eq = expected.rstrip("\n") == out.rstrip("\n")
    print(f"{lid}: code==twin {code_eq} expected==twin_output {exp_eq} stderr_bytes {len(err)} "
          f"lines_out {len(out.splitlines())}")
    ok = ok and code_eq and exp_eq and not err
    for banned in ("import socket", "urllib", "requests", "http", "random", "open("):
        if banned in twin:
            print(f"  {lid}: twin mentions {banned!r}")
print("ALL_OK" if ok else "MISMATCH")
