"""Verifier check (BK4-b round 1): page code equals twin, page expected equals twin stdout, twin runs under -I -W error.

Usage: python3 ledgers/BK4/scripts/BK4-b-r1/twin_page_check.py <repo_root>
Reads only repo files; runs each twin with python -I -W error in a scratch temp dir.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(sys.argv[1]).resolve()
pages = {
    "L04": (root / "course/modules/BK/BK4/L04.html", root / "tests/labs/BK4/lab-BK4-L04-1.py"),
    "L05": (root / "course/modules/BK/BK4/L05.html", root / "tests/labs/BK4/lab-BK4-L05-1.py"),
}
for name, (page, twin) in pages.items():
    text = page.read_text(encoding="utf-8")
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', text, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S)
    twin_src = twin.read_text(encoding="utf-8")
    page_code = html.unescape(code.group(1))
    print(f"{name}: page code bytes {len(page_code)} twin bytes {len(twin_src)} equal={page_code.rstrip(chr(10)) == twin_src.rstrip(chr(10))}")
    with tempfile.TemporaryDirectory() as scratch:
        run = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(twin.resolve())],
            cwd=scratch,
            capture_output=True,
            text=True,
            timeout=60,
        )
    print(f"{name}: exit={run.returncode} stderr={run.stderr!r}")
    page_out = html.unescape(expected.group(1))
    same = page_out.rstrip("\n") == run.stdout.rstrip("\n")
    print(f"{name}: expected block equals twin stdout (exact)={same}")
    if not same:
        import difflib

        for line in difflib.unified_diff(page_out.splitlines(), run.stdout.splitlines(), "page", "twin", lineterm=""):
            print("  " + line)
