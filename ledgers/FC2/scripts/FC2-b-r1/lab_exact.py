"""FC2-b round 1 verifier script: exact lab checks for L04-L06.

For each lab section on the pages L04, L05, L06 of course/modules/FC/FC2:
  1. the page code (HTML-unescaped, <code> body) equals the twin tests/labs/FC2/<id>.py
  2. the twin runs as `python -I -W error <twin>` with exit 0 and empty stderr
  3. the twin's stdout equals the page's expected block EXACTLY (byte-for-byte, after unescaping)
Run from the checkout root:  .venv/bin/python -I ledgers/FC2/scripts/FC2-b-r1/lab_exact.py
"""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(os.getcwd()).resolve()
PAGES = ["L04", "L05", "L06"]
ENV = {"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"}


def sections(page: str) -> list[tuple[str, str, str]]:
    text = (ROOT / "course/modules/FC/FC2" / f"{page}.html").read_text(encoding="utf-8")
    out = []
    for m in re.finditer(r'<section class="lab" id="(lab-FC2-[^"]+)".*?</section>', text, re.S):
        block = m.group(0)
        code = re.search(r"<code[^>]*>(.*?)</code>", block, re.S)
        expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', block, re.S)
        out.append((m.group(1), html.unescape(code.group(1)), html.unescape(expected.group(1))))
    return out


ok_all = True
for page in PAGES:
    for lab_id, code, expected in sections(page):
        twin_path = ROOT / "tests/labs/FC2" / f"{lab_id.replace('lab-', 'lab-')}.py"
        twin = twin_path.read_text(encoding="utf-8")
        same = code.rstrip("\n") == twin.rstrip("\n")
        with tempfile.TemporaryDirectory() as work:
            res = subprocess.run(
                [sys.executable, "-I", "-W", "error", str(twin_path)],
                capture_output=True,
                text=True,
                cwd=work,
                env=ENV,
                timeout=60,
                check=False,
            )
        exact = res.stdout.rstrip("\n") == expected.rstrip("\n")
        clean = res.returncode == 0 and res.stderr == ""
        ok_all &= same and exact and clean
        print(f"{page} {lab_id}: twin_identical={same} exit={res.returncode} stderr_empty={res.stderr == ''} "
              f"stdout_exact={exact} lines={len(res.stdout.splitlines())}")
        if not exact:
            import difflib

            for line in difflib.unified_diff(
                expected.splitlines(), res.stdout.splitlines(), "page_expected", "twin_stdout", lineterm=""
            ):
                print("   ", line)
        if not same:
            import difflib

            for line in list(difflib.unified_diff(
                twin.rstrip("\n").splitlines(), code.rstrip("\n").splitlines(), "twin", "page", lineterm=""
            ))[:40]:
                print("   ", line)
print("ALL EXACT" if ok_all else "MISMATCH")
