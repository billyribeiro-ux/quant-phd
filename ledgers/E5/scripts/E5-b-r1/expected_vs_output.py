"""Run each L04-L06 lab twin under python -I -W error and diff stdout against the page's expected block.

Usage: python3 -I ledgers/E5/scripts/E5-b-r1/expected_vs_output.py <checkout-root>
Prints, per lab, the exit code, stderr size, and the number of differing lines (0 means byte-identical).
"""
import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
for n in ("04", "05", "06"):
    page = (root / f"course/modules/E/E5/L{n}.html").read_text(encoding="utf-8")
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S).group(1)
    exp = html.unescape(exp)
    twin = root / f"tests/labs/E5/lab-E5-L{n}-1.py"
    r = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin)],
        capture_output=True, text=True, cwd="/tmp", env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"},
    )
    out = r.stdout
    diff = [d for d in difflib.unified_diff(exp.splitlines(), out.splitlines(), lineterm="", n=0)
            if not d.startswith(("---", "+++", "@@"))]
    print(f"L{n}: exit={r.returncode} stderr_bytes={len(r.stderr)} out_lines={len(out.splitlines())} "
          f"exp_lines={len(exp.splitlines())} differing_lines={len(diff)}")
    for d in diff[:20]:
        print("   ", d)
    print("   output (verbatim):")
    print("\n".join("      " + x for x in out.splitlines()))
