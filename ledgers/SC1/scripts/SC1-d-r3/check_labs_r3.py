"""Check SC1 project labs: page code equals the twin, the twin runs alone under python -I -W error, and the expected
block equals the twin's stdout. Usage: python check_labs_r3.py <repo-root>"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
page = (root / "course/modules/SC/SC1/project.html").read_text(encoding="utf-8")
labs = {}
for m in re.finditer(r'<section class="lab[^"]*" id="(lab-SC1-project-\d)"', page):
    body = page[m.end() :]
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
    labs[m.group(1)] = (html.unescape(code.group(1)), html.unescape(expected.group(1)))
ok = True
for lab_id, (code, expected) in labs.items():
    n = lab_id[-1]
    twin_path = root / f"tests/labs/SC1/lab-SC1-project-{n}.py"
    twin = twin_path.read_text(encoding="utf-8")
    same = code.strip("\n") == twin.strip("\n")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True)
    out_ok = run.stdout.strip() == expected.strip()
    print(f"{lab_id}: page_code_equals_twin={same} twin_exit={run.returncode} expected_equals_stdout={out_ok}")
    if run.stderr:
        print("  stderr:", run.stderr.strip()[:300])
    if not out_ok:
        print("  stdout:\n" + run.stdout)
        print("  expected:\n" + expected)
    ok &= same and run.returncode == 0 and out_ok
print("ALL OK" if ok else "MISMATCH")
