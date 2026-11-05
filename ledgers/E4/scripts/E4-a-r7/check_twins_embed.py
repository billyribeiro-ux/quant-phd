"""Verifier check (E4 slice a, round 7): page lab code and expected block against the twins.

For each of L01, L02, L03: the <pre><code data-run> text of the page must equal the twin file byte for byte
(after HTML unescaping), and the <pre class="expected"> text must equal the stdout of running the twin with
python -I -W error from the scratch directory /tmp. Exit 0 only when every comparison is True.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
SCRATCH = Path("/tmp")
PAGES = {"L01": "lab-E4-L01-1", "L02": "lab-E4-L02-1", "L03": "lab-E4-L03-1"}

all_ok = True
for lesson, twin_id in PAGES.items():
    page = (ROOT / "course/modules/E/E4" / f"{lesson}.html").read_text(encoding="utf-8")
    twin_path = ROOT / "tests/labs/E4" / f"{twin_id}.py"
    twin = twin_path.read_text(encoding="utf-8")
    code_match = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    exp_match = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(code_match.group(1)) if code_match else None
    expected = html.unescape(exp_match.group(1)) if exp_match else None
    run = subprocess.run(
        [str(ROOT / ".venv/bin/python"), "-I", "-W", "error", str(twin_path)],
        cwd=str(SCRATCH),
        capture_output=True,
        text=True,
        check=False,
    )
    out_ok = run.stdout.rstrip("\n") == (expected or "").rstrip("\n")
    code_ok = (code or "").rstrip("\n") == twin.rstrip("\n")
    print(f"{lesson} exit={run.returncode} stderr_empty={run.stderr == ''} code_equals_twin={code_ok} "
          f"expected_equals_output={out_ok}")
    if run.returncode != 0 or run.stderr or not code_ok or not out_ok:
        all_ok = False
print("ALL_OK" if all_ok else "MISMATCH")
