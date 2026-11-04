"""Verifier script (E4 slice a, round 3): run each lab twin alone and compare the page to the twin.

Usage: python -I -W error check_twins_embed.py <checkout-root>
Runs each twin as `python -I -W error <twin>` from a scratch directory (cwd /tmp, PATH only, no network),
then checks that the page's data-run code equals the twin file and the page's expected block equals the twin stdout.
"""

from __future__ import annotations

import html
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
PAGES = {
    "L01": "lab-E4-L01-1",
    "L02": "lab-E4-L02-1",
    "L03": "lab-E4-L03-1",
}
SCRATCH = Path("/tmp")
ENV = {"PATH": os.environ.get("PATH", "/usr/bin:/bin")}
all_ok = True
for page, lab in PAGES.items():
    twin = ROOT / "tests" / "labs" / "E4" / f"{lab}.py"
    twin_src = twin.read_text(encoding="utf-8")
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin)],
        cwd=str(SCRATCH),
        env=ENV,
        capture_output=True,
        text=True,
        timeout=60,
    )
    stdout = proc.stdout
    print(f"{lab}: exit={proc.returncode} stderr_bytes={len(proc.stderr.encode())} stdout_lines={stdout.count(chr(10))}")
    page_html = (ROOT / "course" / "modules" / "E" / "E4" / f"{page}.html").read_text(encoding="utf-8")
    code_m = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', page_html, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page_html, re.S)
    code_page = html.unescape(code_m.group(1)) if code_m else None
    exp_page = html.unescape(exp_m.group(1)) if exp_m else None
    code_eq = code_page is not None and code_page.rstrip("\n") == twin_src.rstrip("\n")
    exp_eq = exp_page is not None and exp_page.rstrip("\n") == stdout.rstrip("\n")
    print(f"  page code == twin: {code_eq}; page expected == twin stdout: {exp_eq}")
    all_ok = all_ok and proc.returncode == 0 and len(proc.stderr) == 0 and code_eq and exp_eq
print("ALL_OK" if all_ok else "MISMATCH")
