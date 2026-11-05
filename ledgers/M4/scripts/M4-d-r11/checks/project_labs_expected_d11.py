"""Compare each project.html lab's <pre class="expected"> block with the stdout of its twin run alone under python -I -W error."""

import difflib
import html
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(sys.argv[1]).resolve()
raw = (ROOT / "course/modules/M/M4/project.html").read_text(encoding="utf-8")
blocks = re.findall(
    r'<section class="lab[^"]*" id="(lab-M4-project-\d)".*?<pre class="expected"[^>]*>(.*?)</pre>', raw, re.S
)
for lab, expected_html in blocks:
    expected = html.unescape(expected_html).strip()
    twin = ROOT / "tests/labs/M4" / f"{lab.replace('lab-M4-', 'lab-M4-')}.py"
    scratch = Path(tempfile.mkdtemp(prefix="m4p11"))
    (scratch / "data").mkdir()
    proc = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin)], cwd=scratch, capture_output=True, text=True, check=False
    )
    output = proc.stdout.strip()
    print(lab, "exit", proc.returncode, "stderr bytes", len(proc.stderr), "expected==output:", expected == output)
    if expected != output:
        print("\n".join(difflib.unified_diff(expected.splitlines(), output.splitlines(), lineterm="")))
