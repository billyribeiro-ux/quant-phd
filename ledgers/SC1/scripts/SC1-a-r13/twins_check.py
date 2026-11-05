"""Verify SC1 slice-a lab twins: page code == twin, expected block == stdout.

Each twin runs as `python -I -W error` from an empty scratch directory. Trailing newlines are
normalised (the HTML block and the twin file end with a newline that the page does not repeat).
"""
import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGES = {"L01": "lab-SC1-L01-1", "L02": "lab-SC1-L02-1", "L03": "lab-SC1-L03-1"}
for page, twin in PAGES.items():
    html_text = (ROOT / f"course/modules/SC/SC1/{page}.html").read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', html_text, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', html_text, re.S)
    page_code = html.unescape(code.group(1)).rstrip("\n")
    page_expected = html.unescape(expected.group(1)).rstrip("\n")
    twin_src = (ROOT / f"tests/labs/SC1/{twin}.py").read_text(encoding="utf-8").rstrip("\n")
    with tempfile.TemporaryDirectory() as scratch:
        proc = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/SC1/{twin}.py")],
            cwd=scratch, capture_output=True, text=True,
        )
    stdout = proc.stdout.rstrip("\n")
    print(f"{page} twin={twin} exit={proc.returncode} stderr_empty={proc.stderr == ''}")
    print(f"  page_code == twin: {page_code == twin_src} (page {len(page_code)} chars, twin {len(twin_src)} chars)")
    print(f"  expected == stdout: {page_expected == stdout} (expected lines {len(page_expected.splitlines())}, stdout lines {len(stdout.splitlines())})")
    print("  stdout:")
    print(stdout)
    print()
