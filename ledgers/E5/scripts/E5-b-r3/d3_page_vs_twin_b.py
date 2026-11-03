"""Round 3 verifier: page code equals twin, and page expected block equals the twin's stdout.

Each twin runs as `python -I -W error` in a fresh scratch directory (no data/ files are listed by L04-L06).
Run: .venv/bin/python -I ledgers/E5/scripts/E5-b-r3/d3_page_vs_twin_b.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {"L04": "lab-E5-L04-1", "L05": "lab-E5-L05-1", "L06": "lab-E5-L06-1"}
bad = 0
for page, lab in PAGES.items():
    text = (ROOT / "course/modules/E/E5" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    code_page = html.unescape(m.group(1))
    twin_src = (ROOT / "tests/labs/E5" / f"{lab}.py").read_text(encoding="utf-8")
    eq_code = code_page.rstrip("\n") == twin_src.rstrip("\n")
    exp = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)
    exp = html.unescape(exp)
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "lab.py").write_text(twin_src, encoding="utf-8")
        run = subprocess.run(
            [sys.executable, "-I", "-W", "error", "lab.py"], cwd=td, capture_output=True, text=True, timeout=120
        )
    eq_out = run.stdout.rstrip("\n") == exp.rstrip("\n")
    print(f"{page} {lab}: code_equal={eq_code} exit={run.returncode} stderr_bytes={len(run.stderr.encode())} "
          f"expected_equal_stdout={eq_out} stdout_lines={run.stdout.count(chr(10))}")
    if not (eq_code and eq_out and run.returncode == 0 and not run.stderr):
        bad += 1
print("FAILS:", bad)
sys.exit(1 if bad else 0)
