"""Compare each FC2 L07/L08 lab page block with its twin file and with the twin's stdout.

Run: .venv/bin/python ledgers/FC2/scripts/FC2-c-r4/check_lab_pages.py  (from the checkout root)
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {"L07": "lab-FC2-L07-1", "L08": "lab-FC2-L08-1"}
PY = str(ROOT / ".venv" / "bin" / "python")

ok_all = True
for page, lab in PAGES.items():
    text = (ROOT / "course/modules/FC/FC2" / f"{page}.html").read_text(encoding="utf-8")
    section = re.search(r'<section class="lab" id="%s".*?</section>' % lab, text, re.S)
    assert section, lab
    body = section.group(0)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    assert code and expected
    page_code = html.unescape(code.group(1))
    page_expected = html.unescape(expected.group(1))
    twin = (ROOT / "tests/labs/FC2" / f"{lab}.py").read_text(encoding="utf-8")
    code_equal = page_code.strip("\n") == twin.strip("\n")
    run = subprocess.run([PY, "-I", "-W", "error", str(ROOT / "tests/labs/FC2" / f"{lab}.py")],
                         capture_output=True, text=True, cwd="/tmp/fc2c_r4", check=False)
    out_lines = [ln.rstrip() for ln in run.stdout.splitlines()]
    exp_lines = [ln.rstrip() for ln in page_expected.strip("\n").splitlines()]
    expected_equal = out_lines == exp_lines
    print(f"{page} {lab}: exit={run.returncode} stderr_bytes={len(run.stderr.encode())} "
          f"code_equal_twin={code_equal} expected_equal_stdout={expected_equal} "
          f"stdout_lines={len(out_lines)} expected_lines={len(exp_lines)}")
    if not (code_equal and expected_equal and run.returncode == 0 and not run.stderr):
        ok_all = False
        if not expected_equal:
            for a, b in zip(out_lines, exp_lines):
                if a != b:
                    print("  first differing line:\n   out:", repr(a), "\n   exp:", repr(b))
                    break
print("ALL_EQUAL" if ok_all else "MISMATCH")
sys.exit(0 if ok_all else 1)
