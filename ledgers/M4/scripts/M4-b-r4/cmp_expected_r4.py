"""Compare each slice-b page's expected block and code block with a fresh run of its twin.

Run from any directory: python -I ledgers/M4/scripts/M4-b-r4/cmp_expected_r4.py
The repository root is derived from this file's location, so the check runs on the checkout it sits in.
"""

import difflib
import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[4]
PAIRS = [("L05", "lab-M4-L05-1"), ("L06", "lab-M4-L06-1"), ("L07", "lab-M4-L07-1")]
ok = True
for page, lab in PAIRS:
    src = (ROOT / "course/modules/M/M4" / f"{page}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected = html.unescape(m.group(1)).strip()
    twin_path = ROOT / "tests/labs/M4" / f"{lab}.py"
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)],
        capture_output=True,
        text=True,
        check=True,
        cwd="/",
    )
    out = run.stdout.strip()
    code_m = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', src, re.S)
    code = html.unescape(code_m.group(1)).strip()
    twin = twin_path.read_text(encoding="utf-8").strip()
    same_expected = expected == out
    same_code = code == twin
    ok = ok and same_expected and same_code
    print(page, "expected==run:", same_expected, "code==twin:", same_code, "run lines:", len(out.splitlines()))
    if not same_expected:
        print("\n".join(difflib.unified_diff(expected.splitlines(), out.splitlines(), lineterm="")))
print("ALL EQUAL" if ok else "MISMATCH")
