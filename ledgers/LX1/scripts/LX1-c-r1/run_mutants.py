"""Runs the LX1-c round-1 mutants and the input tests (LX1-c round 1). Usage: python3 -I run_mutants.py <checkout>

For each rung-2 mutant: stdout must equal the expected block that project.html prints under lab-LX1-project-2.
For each lab-3 mutant: stdout must equal the expected block under lab-LX1-project-3 on the embedded snapshot.
Input tests: the original lab-3 twin must raise on a blank GBP cell and on a missing month (the claims in its
docstring), and the blank-skipping mutant must not raise on the same input, so the input tells it apart.
"""
import glob, html, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

ROOT = Path.cwd()
PAGE = (ROOT / "course/modules/LX/LX1/project.html").read_text(encoding="utf-8")
SNAPSHOT = ROOT / "course/assets/data/market/fx_monthly.csv"
PY = sys.executable

def expected(lab_id: str) -> str:
    sec = PAGE[PAGE.index(f'id="{lab_id}"'):]
    m = re.search(r'<pre class="expected"[^>]*>(.*?)</pre>', sec, re.S)
    return html.unescape(m.group(1))

def run(path: Path, workdir: Path) -> subprocess.CompletedProcess:
    return subprocess.run([PY, "-I", "-W", "error", str(path)], cwd=workdir, capture_output=True, text=True, timeout=60)

def scratch(with_data: bool) -> Path:
    d = Path(tempfile.mkdtemp(prefix="lx1c-run-"))
    if with_data:
        (d / "data").mkdir()
        shutil.copy(SNAPSHOT, d / "data" / "fx_monthly.csv")
    return d

exp2 = expected("lab-LX1-project-2")
exp3 = expected("lab-LX1-project-3")
rows = []
for f in sorted(glob.glob(str(ROOT / "ledgers/LX1/mutants/lx1c_m*.py"))):
    name = Path(f).name
    is3 = "lab3" in name
    wd = scratch(is3)
    r = run(Path(f), wd)
    exp = exp3 if is3 else exp2
    killed = (r.returncode != 0) or (r.stdout != exp + "\n" and r.stdout.rstrip("\n") != exp.rstrip("\n"))
    rows.append((name, "KILLED" if killed else "SURVIVED", r.returncode, (r.stdout.splitlines() or [""])[-1:] , r.stderr.strip().splitlines()[-1:] ))
    shutil.rmtree(wd)
for row in rows:
    print(row)

# input tests on the lab-3 twin and the blank-skipping mutant
orig = ROOT / "tests/labs/LX1/lab-LX1-project-3.py"
mut = ROOT / "ledgers/LX1/mutants/lx1c_m10_lab3_blank_cell_skipped.py"
lines = SNAPSHOT.read_text(encoding="utf-8").splitlines(keepends=True)
header, body = lines[0], lines[1:]
# blank a GBP cell in the middle (GBP is column index 6 in the header: month,AUD,CAD,CHF,DKK,EUR,GBP,...)
blank_body = list(body)
idx = 300
cells = blank_body[idx].rstrip("\n").split(",")
cells[6] = ""
blank_body[idx] = ",".join(cells) + "\n"
# drop one month to create a gap
gap_body = body[:200] + body[201:]
for label, content in (("blank_gbp_cell", [header] + blank_body), ("missing_month", [header] + gap_body)):
    d = scratch(False)
    (d / "data").mkdir()
    (d / "data" / "fx_monthly.csv").write_text("".join(content), encoding="utf-8")
    ro = run(orig, d)
    rm = run(mut, d)
    print(label, "original rc", ro.returncode, (ro.stderr.strip().splitlines() or [""])[-1][:160])
    print(label, "blank-skipping mutant rc", rm.returncode, "stdout lines", len(rm.stdout.splitlines()))
    shutil.rmtree(d)
