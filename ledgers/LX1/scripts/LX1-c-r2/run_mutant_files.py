"""LX1-c round 2: run every mutant file in ledgers/LX1/mutants/ against the page expected block of its lab.

Mutant files lx1c_m01..m06 and lx1c_r2n01..n02 target lab 2; lx1c_m07..m09 and lx1c_r2n03..n04 target lab 3.
A mutant is killed when its stdout differs from the expected block or it exits non-zero. Run from the repo root.
"""
import html
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
t = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")


def expected(lab):
    s = t.index(f'id="{lab}"')
    seg = t[s:t.index("</section>", s)]
    return html.unescape(re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', seg, re.S).group(1)).rstrip()


killed = 0
files = sorted(p for p in (ROOT / "ledgers/LX1/mutants").glob("*.py"))
for f in files:
    lab = "lab-LX1-project-2" if ("_rung2" in f.name or "r2n01" in f.name or "r2n02" in f.name) else "lab-LX1-project-3"
    wd = tempfile.mkdtemp(prefix="lx1c-r2-mut-")
    os.makedirs(os.path.join(wd, "data"))
    shutil.copy(ROOT / "course/assets/data/market/fx_monthly.csv", os.path.join(wd, "data", "fx_monthly.csv"))
    shutil.copy(f, os.path.join(wd, "m.py"))
    p = subprocess.run([sys.executable, "-I", "-W", "error", "m.py"], cwd=wd, capture_output=True, text=True, timeout=60)
    k = p.returncode != 0 or p.stdout.rstrip() != expected(lab)
    killed += k
    print(f"{f.name}: target={lab} rc={p.returncode} killed={k}")
    shutil.rmtree(wd)
print(f"killed {killed}/{len(files)}")
