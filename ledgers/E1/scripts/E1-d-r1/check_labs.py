"""Verifier check: project page lab code equals twin; expected block equals twin output under python -I -W error."""
from __future__ import annotations

import difflib
import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGE = ROOT / "course/modules/E/E1/project.html"
text = PAGE.read_text(encoding="utf-8")
labs = re.findall(
    r'<section class="lab[^"]*" id="(lab-E1-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>',
    text,
    flags=re.S,
)
print("labs found:", [l[0] for l in labs])
for lab_id, code_html, expected_html in labs:
    code = html.unescape(code_html)
    expected = html.unescape(expected_html)
    twin = (ROOT / "tests/labs/E1" / f"{lab_id.replace('lab-E1-project-', 'lab-E1-project-')}.py").read_text(encoding="utf-8")
    same = code == twin
    print(f"{lab_id}: page code == twin: {same} (page {len(code)} chars, twin {len(twin)} chars)")
    if not same:
        diff = list(difflib.unified_diff(twin.splitlines(), code.splitlines(), "twin", "page", lineterm=""))
        print("\n".join(diff[:60]))
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(ROOT / "tests/labs/E1" / f"{lab_id}.py")],
                         capture_output=True, text=True, cwd="/tmp", check=False)
    out = run.stdout
    print(f"{lab_id}: twin exit {run.returncode}, stderr={run.stderr!r}")
    print(f"{lab_id}: expected == output: {out.rstrip() == expected.rstrip()}")
    if out.rstrip() != expected.rstrip():
        print("OUTPUT:\n" + out)
        print("EXPECTED:\n" + expected)
