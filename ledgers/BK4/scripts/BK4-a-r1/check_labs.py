"""Verifier script (BK4 slice a, round 1): page code equals twin; expected block equals the twin's output.

Run from the checkout root: .venv/bin/python -I -W error ledgers/BK4/scripts/BK4-a-r1/check_labs.py
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ["L01", "L02", "L03"]
ok = True
for page in PAGES:
    text = (ROOT / "course/modules/BK/BK4" / f"{page}.html").read_text(encoding="utf-8")
    for m in re.finditer(r'<section class="lab" id="([^"]+)"[^>]*>(.*?)</section>', text, re.S):
        lab_id, body = m.group(1), m.group(2)
        code = html.unescape(re.search(r"<code[^>]*data-run[^>]*>(.*?)</code>", body, re.S).group(1))
        expected = html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S).group(1))
        twin_path = ROOT / "tests/labs/BK4" / f"{lab_id}.py"
        twin = twin_path.read_text(encoding="utf-8")
        code_eq = code.rstrip("\n") == twin.rstrip("\n")
        run = subprocess.run(
            [sys.executable, "-I", "-W", "error", str(twin_path)], capture_output=True, text=True, timeout=60
        )
        out = run.stdout
        exp_eq = expected.rstrip("\n") == out.rstrip("\n")
        print(f"{page} {lab_id}: exit={run.returncode} code_equals_twin={code_eq} expected_equals_output={exp_eq}"
              f" stderr_bytes={len(run.stderr)} main_guard={'__name__' in twin} lines={len(out.splitlines())}")
        if not (code_eq and exp_eq and run.returncode == 0):
            ok = False
            if not code_eq:
                print("  first code diff lines:")
            if not exp_eq:
                import difflib
                for line in list(difflib.unified_diff(expected.splitlines(), out.splitlines(), lineterm=""))[:20]:
                    print("   ", line)
print("ALL OK" if ok else "MISMATCH")
