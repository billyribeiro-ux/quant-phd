"""Verifier check (M7 slice a, round 2): page lab code equals the twin, and the expected block equals the twin's output.

Run from the checkout root: python -I -W error ledgers/M7/scripts/M7-a-r2/lab_check.py
Reads course/modules/M/M7/L01..L03.html and tests/labs/M7/lab-M7-Lnn-1.py; runs each twin in a subprocess with
python -I -W error and compares its stdout with the page's expected block.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PAGES = ["L01", "L02", "L03"]
for page in PAGES:
    text = (ROOT / f"course/modules/M/M7/{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    e = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    assert m and e, page
    page_code = html.unescape(m.group(1))
    expected = html.unescape(e.group(1))
    twin_path = ROOT / f"tests/labs/M7/lab-M7-{page}-1.py"
    twin = twin_path.read_text(encoding="utf-8")
    code_equal = page_code.rstrip("\n") == twin.rstrip("\n")
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, timeout=60
    )
    out = proc.stdout
    expected_equal = expected.rstrip("\n") == out.rstrip("\n")
    print(f"{page}: exit={proc.returncode} page_code_equals_twin={code_equal} expected_equals_output={expected_equal}")
    print(f"  stderr={proc.stderr!r}")
    print(f"  output_lines={len(out.splitlines())} expected_lines={len(expected.splitlines())}")
    if not expected_equal:
        print("  DIFF:")
        for a, b in zip(expected.splitlines(), out.splitlines()):
            if a != b:
                print(f"    expected={a!r}\n    output  ={b!r}")
