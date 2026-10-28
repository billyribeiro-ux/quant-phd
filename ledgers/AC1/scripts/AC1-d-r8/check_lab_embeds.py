"""Compares each project lab's embedded code and expected output on project.html with its pytest twin, and runs both."""

from __future__ import annotations

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path("/tmp/verify8-AC1-d")
PAGE = (ROOT / "course/modules/AC/AC1/project.html").read_text(encoding="utf-8")
PY = str(ROOT / ".venv/bin/python")
for lab_id in ("lab-AC1-project-1", "lab-AC1-project-2", "lab-AC1-project-3"):
    m = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?<pre><code[^>]*data-run>(.*?)</code></pre>', PAGE, re.S)
    code = html.unescape(m.group(1))
    exp = re.search(rf'id="{lab_id}".*?<pre class="expected"[^>]*>(.*?)</pre>', PAGE, re.S).group(1)
    expected = html.unescape(exp)
    twin = (ROOT / f"tests/labs/AC1/{lab_id}.py").read_text(encoding="utf-8")
    same = code.strip() == twin.strip()
    scratch = pathlib.Path(f"/tmp/AC1-v7/AC1-d/labs/{lab_id}")
    scratch.mkdir(parents=True, exist_ok=True)
    (scratch / "embedded.py").write_text(code, encoding="utf-8")
    run = subprocess.run([PY, "-I", "-W", "error", str(scratch / "embedded.py")], capture_output=True, text=True, cwd=scratch)
    out = run.stdout
    print(f"{lab_id}: embedded==twin {same}; exit {run.returncode}; stdout==page expected: {out.strip() == expected.strip()}")
    if out.strip() != expected.strip():
        print("ACTUAL:\n" + out)
        print("EXPECTED:\n" + expected)
    tw = subprocess.run([PY, "-I", "-W", "error", str(ROOT / f"tests/labs/AC1/{lab_id}.py")], capture_output=True, text=True, cwd=scratch)
    print(f"  twin alone: exit {tw.returncode}; stdout==expected: {tw.stdout.strip() == expected.strip()}; stderr: {tw.stderr.strip()[:200]}")
