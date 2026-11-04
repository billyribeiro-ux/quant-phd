"""Round-8 verifier (M3 slice d): page code of each project lab against its twin, twin stdout against the expected block.

Run from the checkout root: .venv/bin/python -I ledgers/M3/scripts/M3-d-r8/project_labs_r8.py
Prints one line per lab. Exit 0 only when every check holds.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path.cwd()
PAGE = (ROOT / "course/modules/M/M3/project.html").read_text(encoding="utf-8")
PY = sys.executable
bad = 0
for lab in ["lab-M3-project-1", "lab-M3-project-2", "lab-M3-project-3"]:
    m = re.search(r'<section class="lab[^"]*" id="%s".*?</section>' % lab, PAGE, re.S)
    assert m, lab
    sec = m.group(0)
    code = re.search(r'<code class="language-python" data-run>(.*?)</code>', sec, re.S).group(1)
    code = html.unescape(code)
    exp = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S).group(1))
    twin = (ROOT / "tests/labs/M3" / f"{lab}.py").read_text(encoding="utf-8")
    same = code.strip("\n") == twin.strip("\n")
    diff_lines = [
        (i, a, b)
        for i, (a, b) in enumerate(zip(twin.splitlines(), code.splitlines()), 1)
        if a != b
    ]
    run = subprocess.run([PY, "-I", "-W", "error", str(ROOT / "tests/labs/M3" / f"{lab}.py")],
                         capture_output=True, text=True, timeout=60)
    out = run.stdout
    out_ok = out.strip() == exp.strip()
    print(f"{lab}: page==twin {same}; differing lines {len(diff_lines)}; twin exit {run.returncode}; "
          f"stdout==expected {out_ok}; stderr {run.stderr.strip()[:200]!r}")
    for i, a, b in diff_lines[:5]:
        print(f"   line {i}: twin={a!r} page={b!r}")
    if not out_ok:
        print("   stdout:\n" + out)
        print("   expected:\n" + exp)
    print(f"   twin ends with bare main(): {twin.rstrip().endswith('main()')}")
    if not same or run.returncode != 0 or not out_ok:
        bad += 1
print("project labs:", "PASS" if bad == 0 else f"FAIL ({bad})")
sys.exit(1 if bad else 0)
