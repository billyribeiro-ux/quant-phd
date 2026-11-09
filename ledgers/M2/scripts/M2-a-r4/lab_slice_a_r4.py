"""Slice a round 3: page code equals twin, expected block equals twin output, twins run alone under python -I -W error.

Usage: python -I -W error ledgers/M2/scripts/M2-a-r3/lab_slice_a_r3.py <checkout-root>
Reads course/modules/M/M2/L01..L06.html and tests/labs/M2/lab-M2-L0n-1.py, runs each twin from an empty
temporary directory with python -I -W error, and compares stdout with the page's expected block.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1])
py = sys.executable
ok = True
for n in range(1, 7):
    page = root / f"course/modules/M/M2/L{n:02d}.html"
    twin = root / f"tests/labs/M2/lab-M2-L{n:02d}-1.py"
    text = page.read_text(encoding="utf-8")
    m_code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    m_exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    code = html.unescape(m_code.group(1))
    expected = html.unescape(m_exp.group(1))
    twin_src = twin.read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin_src.rstrip("\n")
    with tempfile.TemporaryDirectory() as tmp:
        run = subprocess.run(
            [py, "-I", "-W", "error", str(twin)],
            cwd=tmp,
            capture_output=True,
            text=True,
            timeout=60,
        )
    same_out = run.stdout.rstrip("\n") == expected.rstrip("\n")
    status = run.returncode == 0 and run.stderr == "" and same_code and same_out
    ok = ok and status
    print(
        f"L{n:02d}: code==twin {same_code}; exit {run.returncode}; stderr bytes {len(run.stderr)}; "
        f"stdout==expected {same_out}; PASS {status}"
    )
    if not same_out:
        print("--- expected ---")
        print(expected)
        print("--- got ---")
        print(run.stdout)
print("ALL PASS" if ok else "FAILURES")
