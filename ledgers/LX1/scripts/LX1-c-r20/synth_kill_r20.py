"""LX1-c round 20: survivors of the embedded-snapshot run get a distinguishing input. For each survivor, generate synthetic
GBP series (669 months, 1971-01..2026-09, 4-6 significant digits, with exact repeats and tiny moves, optional blank cell),
run the twin and the mutant under python -I -W error in a scratch dir, and report the first seed where they differ.
Synthetic data is a test input only; it is not presented as data. Usage: python -I synth_kill_r20.py <root> <scratch>"""
import csv
import random
import shutil
import subprocess
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
twin = root / "tests/labs/LX1/lab-LX1-project-3.py"
mut_dir = root / "ledgers/LX1/mutants"
survivors = ["lx1c_r18n02_lab3_difference_of_printed_sds.py", "lx1c_r18n03_lab3_zero_change_tested_after_rounding_to_four_places.py",
             "lx1c_r18n04_lab3_window_two_centred_on_window_one_mean.py", "lx1c_r18n05_lab3_blank_cell_carried_forward_as_flat_rate.py",
             "r17n01_lab3_blank_gbp_cell_read_as_zero.py", "lx1c_r20n04_lab3_zero_test_with_tolerance.py"]
months = []
y, m = 1971, 1
while (y, m) <= (2026, 9):
    months.append(f"{y:04d}-{m:02d}")
    m += 1
    if m == 13:
        y, m = y + 1, 1


def make(seed: int, blank: bool) -> None:
    rng = random.Random(seed)
    rate = 1.5 + rng.random()
    values = []
    for i, _ in enumerate(months):
        r = rng.random()
        if r < 0.05:
            pass  # exact repeat of the previous rate
        elif r < 0.10:
            rate *= 1 + rng.uniform(-1e-7, 1e-7)  # tiny move
        else:
            rate *= 1 + rng.gauss(0, 0.01)
        values.append(f"{rate:.6g}")
    if blank:
        values[rng.randrange(1, len(values))] = ""
    with (scratch / "data" / "fx_monthly.csv").open("w", newline="", encoding="utf-8") as h:
        w = csv.writer(h)
        w.writerow(["month", "GBP"])
        for mo, v in zip(months, values):
            w.writerow([mo, v])


def run(path: Path):
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], capture_output=True, text=True, cwd=str(scratch), timeout=300)
    return r.returncode, r.stdout


(scratch / "data").mkdir(parents=True, exist_ok=True)
for name in survivors:
    assert (mut_dir / name).exists(), name
    killer = None
    for seed in range(40):
        blank = "blank" in name
        make(seed, blank)
        if run(twin) != run(mut_dir / name):
            killer = seed
            break
    print(f"{name}: " + (f"KILLED on synthetic seed {killer} (blank={blank})" if killer is not None else "no distinguishing seed in 40"))
