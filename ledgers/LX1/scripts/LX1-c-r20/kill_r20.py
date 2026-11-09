"""LX1-c round 20: run every mutant under python -I -W error in a scratch dir holding data/fx_monthly.csv and compare
its stdout with the expected block of the page for the lab it mutates (the lab number is read from its docstring).
A mutant is KILLED when rc != 0 or stdout differs from the expected block. Usage: python -I kill_r20.py <root> <scratch>"""
import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
page = (root / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
expected = [html.unescape(x).rstrip("\n") for x in re.findall(r'<pre class="expected"[^>]*>(.*?)</pre>', page, re.S)]
(scratch / "data").mkdir(parents=True, exist_ok=True)
shutil.copy(root / "course/assets/data/market/fx_monthly.csv", scratch / "data" / "fx_monthly.csv")
killed = survived = 0
for mut in sorted((root / "ledgers/LX1/mutants").glob("*.py")):
    text = mut.read_text(encoding="utf-8")
    m = re.search(r"project lab (\d)", text)
    lab = int(m.group(1)) if m else None
    if lab is None:
        # fall back to the docstring first line
        first = text.split("\n", 1)[0]
        m2 = re.search(r"lab (\d)", first)
        lab = int(m2.group(1)) if m2 else 0
    if lab not in (1, 2, 3):
        print("UNMAPPED", mut.name)
        continue
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(mut)], capture_output=True, text=True, cwd=str(scratch), timeout=120)
    out = run.stdout.rstrip("\n")
    differs = out != expected[lab - 1]
    if run.returncode != 0 or differs:
        killed += 1
        how = f"rc={run.returncode} stderr_tail={run.stderr.strip().splitlines()[-1:] if run.stderr.strip() else []}" if run.returncode else "expected-block differs"
        print(f"KILLED lab{lab} {mut.name} | {how}")
    else:
        survived += 1
        print(f"SURVIVED lab{lab} {mut.name}")
print("killed", killed, "survived", survived)
