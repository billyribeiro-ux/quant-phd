"""Round 14, FC1-c: compare each project lab's page code with its twin and its expected block with the twin's output.

Usage: python -I ledgers/FC1/scripts/FC1-c-r14/compare_labs_r14.py
Lab 1 and Lab 3 page code must equal the twin exactly. Lab 2 page code must equal the twin except on lines that
contain the blank ___. Each expected block must equal the stdout of the twin run under python -I -W error.
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGE = (ROOT / "course/modules/FC/FC1/project.html").read_text(encoding="utf-8")
PY = sys.executable
bad = 0
for n in (1, 2, 3):
    lab_id = f"lab-FC1-project-{n}"
    section = re.search(rf'<section[^>]*id="{lab_id}".*?</section>', PAGE, re.S)
    assert section, lab_id
    body = section.group(0)
    code = html.unescape(re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S).group(1))
    expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
    twin = (ROOT / f"tests/labs/FC1/{lab_id}.py").read_text(encoding="utf-8")
    page_lines, twin_lines = code.rstrip("\n").split("\n"), twin.rstrip("\n").split("\n")
    diffs = []
    if len(page_lines) != len(twin_lines):
        diffs.append(f"line count page={len(page_lines)} twin={len(twin_lines)}")
    else:
        for i, (a, b) in enumerate(zip(page_lines, twin_lines), start=1):
            if a != b and "___" not in a:
                diffs.append(f"line {i} differs without a blank")
    run = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/FC1/{lab_id}.py")],
                         capture_output=True, text=True, check=False)
    out_ok = run.stdout.rstrip("\n") == expected.rstrip("\n")
    blanks = sum(line.count("___") for line in page_lines)
    print(f"{lab_id}: page-vs-twin diffs={diffs or 'none'}; blanks on page={blanks}; "
          f"twin run exit={run.returncode}; expected block equals twin output={out_ok}")
    if diffs or run.returncode or not out_ok:
        bad += 1
sys.exit(1 if bad else 0)
