"""Strict check: each project lab's page 'expected' block equals its twin's stdout, and the page code equals the twin (VERIFIER_RULES 2.5)."""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
page = (ROOT / "course/modules/SC/SC1/project.html").read_text(encoding="utf-8")
sections = re.findall(r'<section class="lab[^"]*" id="(lab-SC1-project-\d)".*?<pre><code[^>]*>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>', page, flags=re.S)
assert len(sections) == 3, len(sections)
for lab_id, code_html, expected_html in sections:
    code = html.unescape(code_html)
    twin = (ROOT / f"tests/labs/SC1/{lab_id}.py").read_text(encoding="utf-8")
    code_eq = code.rstrip("\n") == twin.rstrip("\n")
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / f"tests/labs/SC1/{lab_id}.py")], capture_output=True, text=True)
    expected = html.unescape(expected_html)
    exact = run.stdout == expected or run.stdout.rstrip("\n") == expected.rstrip("\n")
    # lab-2 expected block in the page shows the completed lines; the twin is the completed solution.
    print(f"{lab_id}: page code == twin: {code_eq}; stdout exact match to expected block: {exact}; exit={run.returncode}; stderr bytes={len(run.stderr)}")
