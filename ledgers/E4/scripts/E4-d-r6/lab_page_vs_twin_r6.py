"""Compare each project lab's code and expected block on project.html with its twin and the twin's real output.

Usage: python -I lab_page_vs_twin_r6.py <checkout-root>
Prints one line per lab: code-equal (completion lab: every page line equals its twin line or contains a blank),
expected-equal (page expected block == stdout of the twin run alone under python -I -W error).
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
page = (root / "course/modules/E/E4/project.html").read_text(encoding="utf-8")
ok_all = True
for n in (1, 2, 3):
    lab_id = f"lab-E4-project-{n}"
    m = re.search(rf'<section class="lab[^"]*" id="{lab_id}".*?</section>', page, re.S)
    assert m, lab_id
    sec = m.group(0)
    code_m = re.search(r"<pre><code[^>]*>(.*?)</code></pre>", sec, re.S)
    exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S)
    assert code_m and exp_m, lab_id
    code = html.unescape(code_m.group(1)).rstrip("\n").split("\n")
    expected = html.unescape(exp_m.group(1)).rstrip("\n")
    twin_path = root / "tests/labs/E4" / f"{lab_id}.py"
    twin = twin_path.read_text(encoding="utf-8").rstrip("\n").split("\n")
    completion = 'class="lab completion"' in sec[:200]
    if completion:
        code_ok = len(code) == len(twin) and all(p == t or "___" in p for p, t in zip(code, twin))
        blanks = [p for p, t in zip(code, twin) if p != t]
    else:
        code_ok = code == twin
        blanks = []
    run = subprocess.run(
        [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, check=False
    )
    out = run.stdout.rstrip("\n")
    exp_ok = out == expected and run.returncode == 0
    ok_all = ok_all and code_ok and exp_ok
    print(
        f"{lab_id}: completion={completion} code_equal_twin={code_ok} expected_equal_output={exp_ok} "
        f"exit={run.returncode} page_lines={len(code)} twin_lines={len(twin)} blank_lines={blanks}"
    )
print("ALL PASS" if ok_all else "MISMATCH")
