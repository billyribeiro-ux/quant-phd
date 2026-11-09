"""Round 23 (LX1-c): synthetic inputs (test data only, not data) that the embedded snapshot does not contain, run against
the survivors of kill_all_r21.py. Each mutant is compared with the project lab 3 twin on the same CSV.
Inputs: blank_cell (a blank GBP cell in 2010-06), tiny_move (a 1e-5 relative move at month 100),
drift (window-two rates grow 1 percent a month, window one is flat until 1999-12),
Usage: python -I synth_kill_r21.py <repo_root> <scratch>"""
import csv
import subprocess
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
(scratch / "data").mkdir(parents=True, exist_ok=True)
src = list(csv.reader((root / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8", newline="")))
header, body = src[0], src[1:]
g = header.index("GBP")


def write(name, rows):
    with (scratch / "data" / "fx_monthly.csv").open("w", newline="", encoding="utf-8") as h:
        csv.writer(h).writerows([header] + rows)


def run(p):
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True,
                       cwd=str(scratch), timeout=300)
    return r.returncode, r.stdout, r.stderr.strip().splitlines()[-1:] if r.stderr.strip() else []


mutants = {
    "blank_cell": [
        "ledgers/LX1/mutants/r17n01_lab3_blank_gbp_cell_read_as_zero.py",
        "ledgers/LX1/mutants/lx1c_r18n05_lab3_blank_cell_carried_forward_as_flat_rate.py",
    ],
    "tiny_move": [
        "ledgers/LX1/mutants/lx1c_r18n03_lab3_zero_change_tested_after_rounding_to_four_places.py",
        "ledgers/LX1/mutants/lx1c_r20n04_lab3_zero_test_with_tolerance.py",
    ],
    "drift": ["ledgers/LX1/mutants/lx1c_r18n04_lab3_window_two_centred_on_window_one_mean.py"],
    "diff_printed": ["ledgers/LX1/mutants/lx1c_r18n02_lab3_difference_of_printed_sds.py"],
}
cases = {}
rows = [list(r) for r in body]
cases["blank_cell"] = [list(r) for r in body]
idx = next(i for i, r in enumerate(rows) if r[0] == "2010-06")
cases["blank_cell"][idx][g] = ""
cases["tiny_move"] = [list(r) for r in body]
rate = 2.0
for i, r in enumerate(cases["tiny_move"]):
    if i == 100:
        rate = rate * (1 + 1e-5)
    r[g] = f"{rate:.12g}"
cases["drift"] = []
rate = 2.0
for r in body:
    y, m = int(r[0][:4]), int(r[0][5:])
    if (y, m) >= (2000, 1):
        rate = rate * 1.01
    cases["drift"].append([r[0]] + [r[c] if c != g else f"{rate:.12g}" for c in range(1, len(header))])
cases["diff_printed"] = [list(r) for r in body]
for case, files in mutants.items():
    write(case, cases[case])
    twin = run(root / "tests/labs/LX1/lab-LX1-project-3.py")
    print(f"case {case}: twin rc {twin[0]} {twin[2]}")
    for mf in files:
        rc, out, err = run(root / mf)
        same = out == twin[1]
        print(f"   {Path(mf).name}: rc {rc} stdout==twin {same} -> {'KILLED' if (rc != 0 or not same) else 'SURVIVED'} {err}")
