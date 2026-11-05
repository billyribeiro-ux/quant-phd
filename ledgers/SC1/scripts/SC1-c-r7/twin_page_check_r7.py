"""Round-7 check for SC1-c: page code equals twin, expected block equals twin stdout, twin runs under python -I -W error.

Run as: python3 -I -W error ledgers/SC1/scripts/SC1-c-r7/twin_page_check_r7.py  (from the checkout root).
It runs each twin from an empty scratch directory (cwd is not the twin directory), with -I -W error.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAIRS = {
    "L07": ROOT / "course/modules/SC/SC1/L07.html",
    "L08": ROOT / "course/modules/SC/SC1/L08.html",
}
TWINS = {
    "L07": ROOT / "tests/labs/SC1/lab-SC1-L07-1.py",
    "L08": ROOT / "tests/labs/SC1/lab-SC1-L08-1.py",
}

for page, path in PAIRS.items():
    text = path.read_text(encoding="utf-8")
    code_m = re.search(r'<code class="language-python" data-run>(.*?)</code>', text, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    assert code_m and exp_m, page
    page_code = html.unescape(code_m.group(1))
    expected = html.unescape(exp_m.group(1))
    twin_code = TWINS[page].read_text(encoding="utf-8")
    same_code = page_code.rstrip() == twin_code.rstrip()
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(TWINS[page])],
            cwd=scratch,
            capture_output=True,
            text=True,
            timeout=120,
        )
    stdout = proc.stdout
    same_out = expected.rstrip() == stdout.rstrip()
    print(f"{page}: twin exit={proc.returncode} stderr_bytes={len(proc.stderr)}")
    print(f"{page}: page code equals twin (trailing whitespace aside): {same_code}")
    print(f"{page}: expected block equals twin stdout: {same_out} (expected lines={len(expected.splitlines())}, stdout lines={len(stdout.splitlines())})")
    if not same_out:
        print("DIFF expected vs stdout:")
        for a, b in zip(expected.splitlines(), stdout.splitlines()):
            if a != b:
                print("  exp:", a)
                print("  out:", b)
