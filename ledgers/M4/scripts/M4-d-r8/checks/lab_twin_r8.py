"""Project labs: the page code block equals its twin, the twin runs under python -I -W error, and the expected block
equals the twin's output (round 8, slice d). Usage: python -I ledgers/M4/scripts/M4-d-r8/checks/lab_twin_r8.py
"""

import html
import pathlib
import re
import subprocess
import sys

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyD8-M4-d")
PAGE = (ROOT / "course/modules/M/M4/project.html").read_text(encoding="utf-8")
blocks = re.findall(
    r'<section class="lab[^"]*" id="(lab-M4-project-\d)".*?<pre><code class="language-python" data-run>(.*?)</code></pre>\s*<pre class="expected"[^>]*>(.*?)</pre>',
    PAGE,
    re.S,
)
for lab_id, code_html, expected_html in blocks:
    code = html.unescape(code_html)
    expected = html.unescape(expected_html)
    twin = ROOT / "tests/labs/M4" / f"lab-M4-project-{lab_id[-1]}.py"
    twin_text = twin.read_text(encoding="utf-8")
    same = code.strip() == twin_text.strip()
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True, check=False)
    out_ok = run.stdout.strip() == expected.strip()
    print(f"{lab_id}: page code == twin: {same}; twin exit {run.returncode} under -I -W error; output == expected: {out_ok}")
    if not out_ok:
        print("  expected:", expected.strip().splitlines()[:3], "\n  got:", run.stdout.strip().splitlines()[:3], run.stderr[-300:])
print("labs found:", len(blocks))
