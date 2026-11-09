"""Verifier check (CS2 slice a, round 1): page code equals twin, expected block equals twin output.

Run from the checkout root with: .venv/bin/python -I ledgers/CS2/scripts/CS2-a-r1/check_twins.py
Reads only repository files. Runs each twin under CPython with -I -W error in a subprocess.
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
PAGES = ["L01", "L02", "L03", "L04"]
PY = str(ROOT / ".venv" / "bin" / "python")

for page in PAGES:
    text = (ROOT / "course/modules/CS/CS2" / f"{page}.html").read_text(encoding="utf-8")
    lab_id = f"lab-CS2-{page}-1"
    section = re.search(r'<section class="lab" id="%s".*?</section>' % lab_id, text, re.S)
    if section is None:
        print(page, "NO LAB SECTION")
        sys.exit(1)
    body = section.group(0)
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    page_code = html.unescape(code.group(1))
    page_expected = html.unescape(expected.group(1))
    twin = (ROOT / "tests/labs/CS2" / f"{lab_id}.py").read_text(encoding="utf-8")
    code_eq = page_code.rstrip("\n") == twin.rstrip("\n")
    run = subprocess.run([PY, "-I", "-W", "error", str(ROOT / "tests/labs/CS2" / f"{lab_id}.py")],
                         capture_output=True, text=True)
    out_eq = run.stdout.rstrip("\n") == page_expected.rstrip("\n")
    print(f"{page}: exit={run.returncode} page_code_equals_twin={code_eq} "
          f"expected_equals_output={out_eq} stderr_bytes={len(run.stderr)} "
          f"page_code_lines={page_code.count(chr(10))} expected_lines={page_expected.count(chr(10))}")
    if not out_eq:
        import difflib
        for line in difflib.unified_diff(page_expected.splitlines(), run.stdout.splitlines(), "expected", "output", lineterm=""):
            print("   ", line)
    if not code_eq:
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), page_code.splitlines(), "twin", "page", lineterm=""):
            print("   ", line)
