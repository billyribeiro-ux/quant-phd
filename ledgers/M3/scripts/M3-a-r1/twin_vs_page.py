"""Verifier script (M3 slice a, round 1): compare each lab twin with the code and expected block on its page.

Usage: python -I -W error ledgers/M3/scripts/M3-a-r1/twin_vs_page.py
Reads only repository files. Prints one line per lab: twin==page code, expected==observed output, run exit code.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAIRS = {
    "L01": ("course/modules/M/M3/L01.html", "tests/labs/M3/lab-M3-L01-1.py"),
    "L02": ("course/modules/M/M3/L02.html", "tests/labs/M3/lab-M3-L02-1.py"),
    "L03": ("course/modules/M/M3/L03.html", "tests/labs/M3/lab-M3-L03-1.py"),
}
ok = True
for name, (page_rel, twin_rel) in PAIRS.items():
    page = (ROOT / page_rel).read_text(encoding="utf-8")
    twin = (ROOT / twin_rel).read_text(encoding="utf-8")
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', page, re.S)
    code_text = html.unescape(code.group(1))
    same_code = code_text.rstrip("\n") == twin.rstrip("\n")
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    expected_text = html.unescape(expected.group(1)).rstrip("\n")
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(ROOT / twin_rel)],
        capture_output=True,
        text=True,
        cwd="/",
        timeout=120,
    )
    observed = run.stdout.rstrip("\n")
    same_out = observed == expected_text
    print(f"{name}: twin==page-code {same_code}; expected==observed {same_out}; exit {run.returncode}; stderr {run.stderr.strip()[:200]!r}")
    if not (same_code and same_out and run.returncode == 0):
        ok = False
        if not same_out:
            print("--- expected\n" + expected_text + "\n--- observed\n" + observed)
print("twin_vs_page", "PASS" if ok else "FAIL")
