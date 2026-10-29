"""Verifier round 3 (E2-d): page code block == lab twin, and expected block == twin output (project labs 1-3).

Usage (repository root): .venv/bin/python -I ledgers/E2/scripts/E2-d-r3/check_labs_r3.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGE = (ROOT / "course/modules/E/E2/project.html").read_text(encoding="utf-8")
sections = re.findall(r'<section class="lab[^"]*" id="(lab-E2-project-\d)"(.*?)</section>', PAGE, flags=re.S)
for lab_id, body in sections:
    code = re.search(r'<pre><code class="language-python" data-run>(.*?)</code></pre>', body, flags=re.S)
    expected = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, flags=re.S)
    twin = (ROOT / "tests/labs/E2" / f"{lab_id.replace('lab-', 'lab-')}.py").read_text(encoding="utf-8")
    page_code = html.unescape(code.group(1)).rstrip("\n") if code else ""
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/E2" / f"{lab_id}.py")],
                         capture_output=True, text=True, check=False)
    exp = html.unescape(expected.group(1)).strip() if expected else ""
    out = run.stdout.strip()
    print(f"{lab_id}: exit={run.returncode} page_code_equals_twin={page_code == twin.rstrip(chr(10))} "
          f"expected_equals_output={exp == out}")
    if page_code != twin.rstrip("\n"):
        print("  twin lines", len(twin.splitlines()), "page lines", len(page_code.splitlines()))
    if exp != out:
        print("  expected:", exp[:200].replace("\n", " | "))
        print("  output  :", out[:200].replace("\n", " | "))
