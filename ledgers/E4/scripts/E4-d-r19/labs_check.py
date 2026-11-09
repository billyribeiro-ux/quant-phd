"""Round 18 (E4-d): page code vs twin, twin run alone under python -I -W error, expected block vs twin stdout.

Run from the checkout root: python -I ledgers/E4/scripts/E4-d-r19/labs_check.py
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PAGE = ROOT / "course/modules/E/E4/project.html"
text = PAGE.read_text(encoding="utf-8")
PY = sys.executable
blocks = re.findall(
    r'<section class="lab[^"]*" id="(lab-E4-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>',
    text,
    flags=re.S,
)
ok = True
for lab_id, code_html, expected_html in blocks:
    code = html.unescape(code_html)
    expected = html.unescape(expected_html)
    twin_path = ROOT / "tests/labs/E4" / f"{lab_id.replace('lab-E4-', 'lab-E4-')}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = code.rstrip(chr(10)) == twin.rstrip(chr(10))
    diff_lines = []
    if not same:
        import difflib

        diff_lines = list(difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm="", n=0))
    r = subprocess.run(
        [PY, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp", check=False
    )
    out_ok = r.stdout.rstrip(chr(10)) == expected.rstrip(chr(10))
    print(f"{lab_id}: page_code_equals_twin={same} twin_exit={r.returncode} stderr_bytes={len(r.stderr.encode())} "
          f"expected_equals_stdout={out_ok} stdout_lines={r.stdout.count(chr(10))}")
    if diff_lines:
        print("  diff (twin -> page):")
        for line in diff_lines[:20]:
            print("   ", line)
    if not out_ok:
        import difflib as dl

        for line in list(dl.unified_diff(expected.splitlines(), r.stdout.splitlines(), "expected", "stdout", lineterm="", n=0))[:20]:
            print("   ", line)
    ok = ok and r.returncode == 0 and out_ok and r.stderr == ""
print("ALL_LABS_OK" if ok else "LAB_PROBLEM", len(blocks), "labs")
