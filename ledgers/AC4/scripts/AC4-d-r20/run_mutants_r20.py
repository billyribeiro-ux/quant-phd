"""Round 20: run every lab-twin mutant in ledgers/AC4/mutants/ and compare stdout with the page's embedded output.

Usage: run_mutants_r20.py <checkout>. Prints one line per mutant: file, page, exit code, killed-by-output (bool).
A mutant is killed when it exits nonzero or its stdout differs from the embedded expected block of its page.
"""

import html
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(sys.argv[1])
PY = str(ROOT / ".venv/bin/python")
expected = {}
for lab in ("L07", "L08"):
    src = (ROOT / f"course/modules/AC/AC4/{lab}.html").read_text(encoding="utf-8")
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', src, re.S)
    expected[lab] = html.unescape(m.group(1)).strip()
mut_root = ROOT / "ledgers/AC4/mutants"
files = sorted(p for p in mut_root.rglob("*.py"))
for f in files:
    text = f.read_text(encoding="utf-8")
    m = re.search(r"AC4-L0([78])", text)
    page = f"L0{m.group(1)}" if m else "?"
    proc = subprocess.run([PY, "-I", "-W", "error", str(f)], capture_output=True, text=True, cwd="/tmp/ac4d-r20", timeout=120)
    out = proc.stdout.strip()
    differs = out != expected.get(page, "")
    killed = proc.returncode != 0 or differs
    rel = f.relative_to(mut_root)
    print(f"{rel} | page {page} | exit {proc.returncode} | output_differs {differs} | killed {killed}")
