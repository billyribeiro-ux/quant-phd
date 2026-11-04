"""Verifier check for SC1 slice b (L04-L06): page code equals twin, twin runs cleanly, expected equals output.

Usage: python -I -W error ledgers/SC1/scripts/SC1-b-r2/twin_match.py   (run from the checkout root)
"""

from __future__ import annotations

import html
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PAGES = {
    "L04": ROOT / "course/modules/SC/SC1/L04.html",
    "L05": ROOT / "course/modules/SC/SC1/L05.html",
    "L06": ROOT / "course/modules/SC/SC1/L06.html",
}
ok = True
for page, path in PAGES.items():
    text = path.read_text(encoding="utf-8")
    sections = re.findall(r'<section class="lab" id="(lab-SC1-[^"]+)"[^>]*>(.*?)</section>', text, re.S)
    for lab_id, body in sections:
        code_m = re.search(r'<code class="language-python" data-run>(.*?)</code>', body, re.S)
        exp_m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', body, re.S)
        code = html.unescape(code_m.group(1))
        expected = html.unescape(exp_m.group(1))
        twin = ROOT / "tests/labs/SC1" / f"{lab_id.replace('lab-SC1-', 'lab-SC1-')}.py"
        twin_src = twin.read_text(encoding="utf-8")
        code_eq = code.strip("\n") == twin_src.strip("\n")
        with tempfile.TemporaryDirectory(prefix="v2sc1b-") as scratch:
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
        if not out_eq:
            print("--- output ---")
            print(proc.stdout)
            print("--- expected ---")
            print(expected)
print("ALL MATCH" if ok else "MISMATCH")
