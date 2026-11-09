"""Verifier script (FC1-b round 4): page code == twin, expected == twin stdout, twin run alone.

Usage: python3 -I ledgers/FC1/scripts/FC1-b-r4/twin_vs_page_r4.py <checkout-root>
Runs each twin with `python -I -W error` from a scratch directory outside the repo,
so no local module can shadow the standard library.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PAGES = {
    "L04": ("course/modules/FC/FC1/L04.html", "tests/labs/FC1/lab-FC1-L04-1.py"),
    "L05": ("course/modules/FC/FC1/L05.html", "tests/labs/FC1/lab-FC1-L05-1.py"),
}
PYTHON = ROOT / ".venv" / "bin" / "python"

all_ok = True
for page, (page_rel, twin_rel) in PAGES.items():
    text = (ROOT / page_rel).read_text(encoding="utf-8")
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    assert code_m and exp_m, page
    page_code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin = (ROOT / twin_rel).read_text(encoding="utf-8")
    markers = text.count("@@LAB") + text.count("@@OUT")
    code_equal = page_code.rstrip() == twin.rstrip()
    with tempfile.TemporaryDirectory() as scratch:
        twin_copy = Path(scratch) / Path(twin_rel).name
        twin_copy.write_text(twin, encoding="utf-8")
        run = subprocess.run(
            [str(PYTHON), "-I", "-W", "error", str(twin_copy)],
            cwd=scratch,
            capture_output=True,
            text=True,
            timeout=60,
        )
    stdout_equal = expected.strip() == run.stdout.strip()
    print(
        f"{page}: page_code_bytes {len(page_code)} twin_bytes {len(twin)} page_code_equals_twin {code_equal} "
        f"markers {markers} rc {run.returncode} stderr_bytes {len(run.stderr)} stdout_lines "
        f"{len(run.stdout.splitlines())} expected_equals_stdout {stdout_equal}"
    )
    all_ok = all_ok and code_equal and markers == 0 and run.returncode == 0 and not run.stderr and stdout_equal
print("ALL OK" if all_ok else "MISMATCH")
