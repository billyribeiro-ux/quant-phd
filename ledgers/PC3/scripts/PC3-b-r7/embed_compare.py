"""Compares, for L04, L05, L06: page lab code == twin (trailing newline stripped); expected block == twin stdout.

Also runs each twin alone under python -I -W error and reports rc and stderr size.
Run from the checkout root: .venv/bin/python -I ledgers/PC3/scripts/PC3-b-r7/embed_compare.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
PY = str(ROOT / ".venv" / "bin" / "python")
PAGES = {"L04": "lab-PC3-L04-1.py", "L05": "lab-PC3-L05-1.py", "L06": "lab-PC3-L06-1.py"}

for page, twin_name in PAGES.items():
    text = (ROOT / f"course/modules/PC/PC3/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', text, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', text, re.S).group(1)
    twin = (ROOT / "tests/labs/PC3" / twin_name).read_text(encoding="utf-8")
    page_code = html.unescape(code).rstrip("\n")
    twin_code = twin.rstrip("\n")
    proc = subprocess.run(
        [PY, "-I", "-W", "error", str(ROOT / "tests/labs/PC3" / twin_name)],
        capture_output=True,
        text=True,
        timeout=60,
        cwd="/tmp",
    )
    out = proc.stdout.rstrip("\n")
    exp = html.unescape(expected).rstrip("\n")
    print(f"{page}: page code == twin: {page_code == twin_code} (page {len(page_code)} chars, twin {len(twin_code)})")
    print(f"{page}: expected == twin stdout: {exp == out} (expected lines {len(exp.splitlines())}, stdout lines {len(out.splitlines())})")
    print(f"{page}: twin alone rc={proc.returncode} stderr_bytes={len(proc.stderr.encode())}")
    (ROOT / f"ledgers/PC3/scripts/PC3-b-r7/out/{page}.stdout").write_text(out + "\n", encoding="utf-8")
