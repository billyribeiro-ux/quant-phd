"""LX1-c round 20: one synthetic input with a single 1e-10 relative move at month index 100 (a test input, not data).
Compares the twin and the tolerance mutant (lx1c_r20n04) on it. Usage: python -I tiny_move_r20.py <root> <scratch>"""
import csv
import subprocess
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
(scratch / "data").mkdir(parents=True, exist_ok=True)
months = []
y, m = 1971, 1
while (y, m) <= (2026, 9):
    months.append(f"{y:04d}-{m:02d}")
    m += 1
    if m == 13:
        y, m = y + 1, 1
rows = [["month", "GBP"]]
rate = 2.0
for i, mo in enumerate(months):
    if i == 100:
        rate = rate * (1 + 1e-10)
    rows.append([mo, f"{rate:.12g}"])
with (scratch / "data" / "fx_monthly.csv").open("w", newline="") as h:
    csv.writer(h).writerows(rows)
def run(p: Path):
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True, cwd=str(scratch), timeout=300)
    return r.returncode, r.stdout
twin = run(root / "tests/labs/LX1/lab-LX1-project-3.py")
mut = run(root / "ledgers/LX1/mutants/lx1c_r20n04_lab3_zero_test_with_tolerance.py")
print("twin rc", twin[0], "mutant rc", mut[0])
for a, b in zip(twin[1].splitlines(), mut[1].splitlines()):
    if a != b:
        print("TWIN  :", a)
        print("MUTANT:", b)
