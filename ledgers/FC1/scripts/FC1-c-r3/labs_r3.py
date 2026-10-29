"""Checks the FC1 project labs: page code equals twin, twin runs under python -I -W error, stdout equals expected block.

Usage: python ledgers/FC1/scripts/FC1-c-r3/labs_r3.py <checkout-root> <out-dir>
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
out = Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
page = (root / "course/modules/FC/FC1/project.html").read_text(encoding="utf-8")
py = root / ".venv/bin/python"
ok = True
for lab in ("project-1", "project-2", "project-3"):
    m = re.search(rf'<section class="lab[^"]*" id="lab-FC1-{lab}".*?<pre><code[^>]*>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin = (root / f"tests/labs/FC1/lab-FC1-{lab}.py").read_text(encoding="utf-8")
    same_as_twin = code.strip() == twin.strip()
    d = out / lab
    d.mkdir(exist_ok=True)
    (d / "page_code.py").write_text(code, encoding="utf-8")
    run = subprocess.run([str(py), "-I", "-W", "error", str(root / f"tests/labs/FC1/lab-FC1-{lab}.py")],
                         capture_output=True, text=True, cwd=str(d))
    stdout_ok = run.stdout.strip() == expected.strip()
    print(f"{lab}: page==twin {same_as_twin} | twin exit {run.returncode} stderr {len(run.stderr)}B | "
          f"stdout==expected {stdout_ok}")
    (d / "stdout.txt").write_text(run.stdout, encoding="utf-8")
    ok = ok and same_as_twin and run.returncode == 0 and not run.stderr and stdout_ok
    if not same_as_twin:
        import difflib
        print("".join(difflib.unified_diff(twin.splitlines(True), code.splitlines(True), "twin", "page")))
print("LABS", "PASS" if ok else "FAIL")
