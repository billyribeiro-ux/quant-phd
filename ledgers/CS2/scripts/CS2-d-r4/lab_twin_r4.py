"""Round-4 lab check for CS2 project labs: page code equals the twin, expected block equals the run (python -I -W error)."""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGE = (ROOT / "course/modules/CS/CS2/project.html").read_text(encoding="utf-8")
PY = str(ROOT / ".venv/bin/python")
rc = 0
for n in (1, 2, 3):
    section = re.search(rf'<section class="lab[^"]*" id="lab-CS2-project-{n}".*?</section>', PAGE, re.S).group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', section, re.S).group(1))
    assert "<span" not in code and "<em" not in code, "unexpected markup inside the code block"
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', section, re.S).group(1))
    twin_path = ROOT / f"tests/labs/CS2/lab-CS2-project-{n}.py"
    twin = twin_path.read_text(encoding="utf-8")
    twin_eq = code.strip() == twin.strip()
    run = subprocess.run([PY, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, check=False)
    out_eq = run.stdout.rstrip() == expected.rstrip()
    print(f"lab {n}: page_code_equals_twin={twin_eq} twin_rc={run.returncode} stdout_equals_expected={out_eq}")
    if run.stderr:
        print("  stderr:", run.stderr.strip()[:300])
    if not (twin_eq and run.returncode == 0 and out_eq):
        rc = 1
        import difflib
        for line in difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm="", n=0):
            print("  ", line)
sys.exit(rc)
