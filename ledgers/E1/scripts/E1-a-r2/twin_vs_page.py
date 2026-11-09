"""Compare each E1 slice-a lab page code block with its twin, and the expected block with the twin's stdout.

Run from the checkout root with: python -I -W error ledgers/E1/scripts/E1-a-r2/twin_vs_page.py
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
PY = sys.executable
PAGES = {"L01": "lab-E1-L01-1", "L02": "lab-E1-L02-1", "L03": "lab-E1-L03-1"}
for page, lab in PAGES.items():
    text = (ROOT / f"course/modules/E/E1/{page}.html").read_text(encoding="utf-8")
    section = re.search(rf'<section class="lab" id="{lab}".*?</section>', text, re.S).group(0)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code></pre>', section, re.S).group(1)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1)
    code = html.unescape(code)
    expected = html.unescape(expected)
    twin = (ROOT / f"tests/labs/E1/{lab}.py").read_text(encoding="utf-8")
    same_code = code == twin
    if not same_code:
        same_code = code.rstrip("\n") == twin.rstrip("\n")
    out = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/E1/{lab}.py")], capture_output=True, text=True)
    same_out = out.stdout.rstrip("\n") == expected.rstrip("\n")
    print(f"{page} {lab}: page_code_equals_twin={same_code} (exact={code == twin}) "
          f"twin_exit={out.returncode} expected_equals_stdout={same_out} stdout_lines={len(out.stdout.splitlines())} "
          f"stderr={out.stderr.strip()!r}")
    if not same_code:
        import difflib
        print("".join(list(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page"))[:40]))
