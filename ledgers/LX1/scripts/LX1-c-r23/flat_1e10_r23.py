"""Round 23 (LX1-c): synthetic kill for lx1c_r20n04 (zero test with tolerance 1e-9). Builds a flat GBP series (2.0 in
every month) with one 1e-10 relative move at row 100, runs the lab 3 twin and the mutant with python -I -W error in a
scratch directory, and prints their zero-change counts. Test data only, not data.
Usage: python -I flat_1e10_r23.py <repo_root> <scratch>"""
import csv
import subprocess
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
(scratch / "data").mkdir(parents=True, exist_ok=True)
rows = list(csv.DictReader(open(root / "course/assets/data/market/fx_monthly.csv", encoding="utf-8")))
header = list(rows[0].keys())
for i, r in enumerate(rows):
    r["GBP"] = "2.0000000002" if i >= 100 else "2.0"
with open(scratch / "data" / "fx_monthly.csv", "w", newline="", encoding="utf-8") as h:
    w = csv.DictWriter(h, fieldnames=header)
    w.writeheader()
    w.writerows(rows)
for label, script in (("twin", root / "tests/labs/LX1/lab-LX1-project-3.py"),
                      ("mutant", root / "ledgers/LX1/mutants/lx1c_r20n04_lab3_zero_test_with_tolerance.py")):
    run = subprocess.run([sys.executable, "-I", "-W", "error", str(script)], capture_output=True, text=True, cwd=str(scratch))
    print(label, "rc", run.returncode, [line.strip() for line in run.stdout.splitlines() if "zero" in line])
