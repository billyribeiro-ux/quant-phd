"""Round 2 check for PC3-b: run each lab twin alone under python -I -W error from a scratch cwd, compare the
page's data-run code with the twin, and compare the page's expected block with the twin's stdout.

Usage: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r2/lab_twin_check.py <checkout>
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
    "L04": ("lab-PC3-L04-1", "course/modules/PC/PC3/L04.html", "tests/labs/PC3/lab-PC3-L04-1.py"),
    "L05": ("lab-PC3-L05-1", "course/modules/PC/PC3/L05.html", "tests/labs/PC3/lab-PC3-L05-1.py"),
    "L06": ("lab-PC3-L06-1", "course/modules/PC/PC3/L06.html", "tests/labs/PC3/lab-PC3-L06-1.py"),
}
PYTHON = str(ROOT / ".venv" / "bin" / "python")

for page, (lab_id, page_path, twin_path) in PAGES.items():
    twin = (ROOT / twin_path).read_text(encoding="utf-8")
    src = (ROOT / page_path).read_text(encoding="utf-8")
    section = re.search(rf'<section class="lab" id="{lab_id}".*?</section>', src, re.S)
    assert section, f"no section {lab_id}"
    body = section.group(0)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    page_code = html.unescape(code.group(1))
    page_expected = html.unescape(expected.group(1))
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run(
            [PYTHON, "-I", "-W", "error", str(ROOT / twin_path)],
            cwd=scratch,
            capture_output=True,
            text=True,
            timeout=120,
        )
    code_equal = page_code.rstrip("\n") == twin.rstrip("\n")
    expected_equal = page_expected.rstrip("\n") == proc.stdout.rstrip("\n")
    print(
        f"{page} twin exit={proc.returncode} stderr_bytes={len(proc.stderr.encode())} "
        f"page_code_equals_twin={code_equal} expected_equals_stdout={expected_equal} "
        f"stdout_lines={len(proc.stdout.splitlines())}"
    )
    if not expected_equal:
        import difflib

        for line in difflib.unified_diff(
            page_expected.rstrip("\n").splitlines(),
            proc.stdout.rstrip("\n").splitlines(),
            "page_expected",
            "twin_stdout",
            lineterm="",
        ):
            print("   ", line)
    if not code_equal:
        import difflib

        for line in difflib.unified_diff(
            twin.rstrip("\n").splitlines(), page_code.rstrip("\n").splitlines(), "twin", "page_code", lineterm=""
        ):
            print("   ", line)
    Path(f"/Users/billyribeiro/.fanout/scratch/PC3-b-r2/twin_{page}_stdout.txt").write_text(proc.stdout, encoding="utf-8")
