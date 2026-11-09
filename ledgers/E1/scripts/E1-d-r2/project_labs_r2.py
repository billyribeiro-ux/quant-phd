"""Verifier round 2, slice d: project labs.

Page code vs twin, twin run under python -I -W error, expected block vs output.

Usage: .venv/bin/python -I ledgers/E1/scripts/E1-d-r2/project_labs_r2.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
page = (ROOT / "course/modules/E/E1/project.html").read_text(encoding="utf-8")
labs = {
    "lab-E1-project-1": "lab-E1-project-1.py",
    "lab-E1-project-2": "lab-E1-project-2.py",
    "lab-E1-project-3": "lab-E1-project-3.py",
}
ok = True
for lab_id, twin_name in labs.items():
    m = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?</section>', page, re.S)
    assert m, lab_id
    sec = m.group(0)
    code_html = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', sec, re.S).group(1)
    exp_html = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1)
    code = html.unescape(code_html)
    expected = html.unescape(exp_html)
    twin = (ROOT / "tests/labs/E1" / twin_name).read_text(encoding="utf-8")
    blanks = code.count("___")
    same_after_fill = code.rstrip("\n") == twin.rstrip("\n")
    diff_lines = [
        (i, p, t) for i, (p, t) in enumerate(zip(code.splitlines(), twin.splitlines(), strict=False), 1) if p != t
    ]
    differing = [i for i, _, _ in diff_lines]
    print(f"{lab_id}: page==twin {same_after_fill}; blanks on page {blanks}; differing lines {differing}")
    for i, p, t in diff_lines:
        print(f"   line {i}: page={p.strip()!r}")
        print(f"           twin={t.strip()!r}")
    if blanks == 0 and not same_after_fill:
        ok = False
    with tempfile.TemporaryDirectory(prefix="e1d-r2-lab-") as d:
        scratch = Path(d)
        (scratch / "twin.py").write_text(twin, encoding="utf-8")
        run = subprocess.run(
            [sys.executable, "-I", "-W", "error", "twin.py"], cwd=scratch, capture_output=True, text=True, check=False
        )
    out = run.stdout.rstrip("\n")
    exp = expected.rstrip("\n")
    same = out == exp
    print(f"   twin exit {run.returncode}; stderr {run.stderr.strip()!r}; output == expected block: {same}")
    if out != exp:
        print("   output:", out.replace("\n", " | "))
        print("   expected:", exp.replace("\n", " | "))
        ok = False
    if run.returncode != 0 or run.stderr.strip():
        ok = False
print("project labs r2 ok:", ok)
