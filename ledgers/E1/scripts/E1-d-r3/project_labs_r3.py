"""Compare each E1 project lab's page code with its twin, and its expected block with the twin's output."""

from __future__ import annotations

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGE = (ROOT / "course/modules/E/E1/project.html").read_text(encoding="utf-8")
PY = str(ROOT / ".venv/bin/python")
for lab in ("project-1", "project-2", "project-3"):
    m = re.search(
        rf'<section class="lab[^"]*" id="lab-E1-{lab}".*?<pre><code class="language-python" data-run>(.*?)</code></pre>'
        rf'\s*<pre class="expected"[^>]*>(.*?)</pre>',
        PAGE,
        re.S,
    )
    assert m, lab
    code = html.unescape(m.group(1))
    expected = html.unescape(m.group(2))
    twin_path = ROOT / f"tests/labs/E1/lab-E1-{lab}.py"
    twin = twin_path.read_text(encoding="utf-8")
    blanks = code.count("___")
    diff = [l for l in difflib.unified_diff(twin.splitlines(), code.splitlines(), lineterm="", n=0)
            if l[:1] in "+-" and not l.startswith(("+++", "---"))]
    run = subprocess.run([PY, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, cwd="/tmp/e1d_r3")
    print(f"{lab}: page-vs-twin differing lines={len(diff)} blanks_on_page={blanks}")
    for l in diff:
        print("   ", l)
    print(f"{lab}: twin exit={run.returncode} stderr_empty={run.stderr == ''}")
    print(f"{lab}: output==expected: {run.stdout.rstrip() == expected.rstrip()}")
    if run.stdout.rstrip() != expected.rstrip():
        print(run.stdout)
        print(expected)
