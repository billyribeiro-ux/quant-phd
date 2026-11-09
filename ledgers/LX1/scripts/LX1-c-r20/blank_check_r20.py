"""LX1-c round 20: blank-cell and month-gap inputs (synthetic test inputs, not data). Runs the twin and the silent-blank
mutants under python -I -W error. Usage: python -I blank_check_r20.py <root> <scratch>"""
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


def write(values, drop=None):
    rows = [["month", "GBP"]] + [[mo, v] for mo, v in zip(months, values)]
    if drop is not None:
        del rows[drop]
    with (scratch / "data" / "fx_monthly.csv").open("w", newline="") as h:
        csv.writer(h).writerows(rows)


def run(p: Path):
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True, cwd=str(scratch), timeout=300)
    return r.returncode, len(r.stdout.splitlines()), (r.stderr.strip().splitlines() or [""])[-1]


base = [f"{2 + i * 1e-3:.4f}" for i in range(len(months))]
blank = list(base)
blank[300] = ""
write(blank)
twin = root / "tests/labs/LX1/lab-LX1-project-3.py"
print("blank cell, twin:", run(twin))
for name in ["r17n01_lab3_blank_gbp_cell_read_as_zero.py", "lx1c_r18n05_lab3_blank_cell_carried_forward_as_flat_rate.py",
             "lx1c_r8n03_lab3_blank_cell_skipped_silently.py"]:
    print("blank cell,", name, ":", run(root / "ledgers/LX1/mutants" / name))
write(base, drop=300)
print("month gap, twin:", run(twin))
print("month gap, lx1c_r8n04:", run(root / "ledgers/LX1/mutants" / "lx1c_r8n04_lab3_month_gap_not_checked.py"))
