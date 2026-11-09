"""Round-18 LX1-c: distinguishing input for the survivor r17n01 (verifier-written).

Copies the real snapshot into a scratch dir, blanks one GBP cell (1985-03) and runs the Lab 3 twin and the
r17n01 mutant under python -I -W error. The twin must fail loudly (page claim, project.html Check paragraph);
the mutant must not, which proves the mutant is distinguishable by a blank-cell input.
Usage: python -I blank_cell_r18.py <checkout_root>
"""
import csv
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(sys.argv[1]).resolve()
SNAP = ROOT / "course/assets/data/market/fx_monthly.csv"
TWIN = ROOT / "tests/labs/LX1/lab-LX1-project-3.py"
MUT = ROOT / "ledgers/LX1/mutants" / sys.argv[2]
with SNAP.open(encoding="utf-8", newline="") as h:
    rows = list(csv.DictReader(h))
    fields = list(rows[0].keys())
for r in rows:
    if r["month"] == "1971-01":
        r["GBP"] = ""
tmp = pathlib.Path(tempfile.mkdtemp(prefix="lx1c_r18_blank_"))
(tmp / "data").mkdir()
with (tmp / "data" / "fx_monthly.csv").open("w", encoding="utf-8", newline="") as h:
    w = csv.DictWriter(h, fieldnames=fields)
    w.writeheader()
    w.writerows(rows)
for name, path in (("twin", TWIN), ("mutant", MUT)):
    p = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], cwd=tmp, capture_output=True, text=True, timeout=120)
    last = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""
    print(f"{name}: rc={p.returncode} stdout_lines={len(p.stdout.splitlines())} stderr_last={last[:160]}")
shutil.rmtree(tmp, ignore_errors=True)
