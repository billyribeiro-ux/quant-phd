"""Round 4 verifier check, SC1 slice b (L04-L06): page code equals twin, twin runs cleanly, expected equals output.

Usage (from checkout root): python -I -W error ledgers/SC1/scripts/SC1-b-r4/twin_match.py
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = ["L04", "L05", "L06"]
ok = True
for page in PAGES:
    path = ROOT / f"course/modules/SC/SC1/{page}.html"
    text = path.read_text(encoding="utf-8")
    sections = re.findall(r'<section class="lab" id="(lab-SC1-[^"]+)"[^>]*>(.*?)</section>', text, re.S)
    print(page, "lab sections:", [s[0] for s in sections])
    for lab_id, body in sections:
        code_m = re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S)
        exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
        code = html.unescape(code_m.group(1))
        expected = html.unescape(exp_m.group(1))
        twin = ROOT / "tests/labs/SC1" / f"{lab_id}.py"
        twin_src = twin.read_text(encoding="utf-8")
        code_eq = code.strip("\n") == twin_src.strip("\n")
        with tempfile.TemporaryDirectory(prefix="v4sc1b-") as scratch:
            proc = subprocess.run(
                [sys.executable, "-I", "-W", "error", str(twin)],
                cwd=scratch,
                capture_output=True,
                text=True,
                timeout=120,
            )
        out_eq = proc.stdout.strip("\n") == expected.strip("\n")
        status = "PASS" if (code_eq and out_eq and proc.returncode == 0 and proc.stderr == "") else "FAIL"
        if status != "PASS":
            ok = False
        print(
            f"{page} {lab_id} twin={twin.name} code_equals_twin={code_eq} exit={proc.returncode} "
            f"stderr_empty={proc.stderr == ''} expected_equals_output={out_eq} -> {status}"
        )
        print("--- output ---")
        print(proc.stdout)
print("ALL MATCH" if ok else "MISMATCH")
