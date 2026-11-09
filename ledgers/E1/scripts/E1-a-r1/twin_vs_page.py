"""Run each E1 lab twin of slice a alone under python -I -W error and compare with the page (verifier round 1).

Checks: (1) the page code block equals the twin text (trailing newlines aside); (2) the twin exits 0 with empty
stderr; (3) the twin's stdout equals the page's expected block, character for character.
Usage: python -I twin_vs_page.py <repo-root>
"""

import html
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(sys.argv[1])
MODULE = ROOT / "course/modules/E/E1"
TWINS = ROOT / "tests/labs/E1"
bad = 0
for page, lab in [("L01", "lab-E1-L01-1"), ("L02", "lab-E1-L02-1"), ("L03", "lab-E1-L03-1")]:
    text = (MODULE / f"{page}.html").read_text(encoding="utf-8")
    section = re.search(rf'<section class="lab" id="{lab}".*?</section>', text, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', section, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1))
    twin = (TWINS / f"{lab}.py").read_text(encoding="utf-8")
    same_code = code.rstrip("\n") == twin.rstrip("\n")
    with tempfile.TemporaryDirectory() as work:
        started = time.perf_counter()
        result = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(TWINS / f"{lab}.py")],
            capture_output=True, text=True, cwd=work, env={"PATH": "/usr/bin:/bin", "PYTHONHASHSEED": "0"}, check=False,
        )
        elapsed = time.perf_counter() - started
    same_out = result.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{lab}: code==twin {same_code}; exit {result.returncode}; stderr {result.stderr!r}; "
          f"stdout==expected {same_out}; {elapsed:.2f}s; lines {len(result.stdout.splitlines())}")
    if not (same_code and result.returncode == 0 and not result.stderr and same_out):
        bad += 1
        print(result.stdout)
print("twin_vs_page failures:", bad)
