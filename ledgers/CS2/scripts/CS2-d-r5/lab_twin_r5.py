# ruff: noqa: E501
"""Round-5 verifier (CS2-d): project lab check. Page code vs twin, twin run under python -I -W error, expected vs stdout.

Lab 2 is a completion lab: the page code must differ from the twin only at the lines that contain the blank ___.
"""

from __future__ import annotations

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PAGE = (ROOT / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
PY = str(ROOT / ".venv/bin/python")
rc = 0
for n in (1, 2, 3):
    section = re.search(rf'<section class="lab[^"]*" id="lab-CS2-project-{n}".*?</section>', PAGE, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', section, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1))
    twin_path = ROOT / f"tests/labs/CS2/lab-CS2-project-{n}.py"
    twin = twin_path.read_text(encoding="utf-8")
    run = subprocess.run([PY, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, check=False)
    out_eq = run.stdout.rstrip() == expected.rstrip()
    diff = [
        line
        for line in difflib.unified_diff(twin.strip().splitlines(), code.strip().splitlines(), lineterm="", n=0)
        if line[:1] in "+-" and not line.startswith(("+++", "---"))
    ]
    blanks_only = all("___" in line for line in diff if line.startswith("+")) if n == 2 else not diff
    print(
        f"lab {n}: twin_rc={run.returncode} stdout_equals_expected={out_eq} page_vs_twin_diff_lines={len(diff)} "
        f"differences_are_blanks_only={blanks_only}"
    )
    for line in diff:
        print("   ", line[:160])
    if run.stderr:
        print("  stderr:", run.stderr.strip()[:300])
    if not (run.returncode == 0 and out_eq and blanks_only):
        rc = 1
print("RESULT", "PASS" if rc == 0 else "FAIL")
sys.exit(rc)
