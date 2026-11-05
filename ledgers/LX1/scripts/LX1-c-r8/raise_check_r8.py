"""Round 8: run the lab 3 twin and the two new survivor mutants on a damaged snapshot (blank GBP cell; skipped month).

Scratch directories only. The committed snapshot is read, copied, and never written."""

import csv
import pathlib
import subprocess
import sys
import tempfile

ROOT = pathlib.Path("/Users/billyribeiro/.fanout/wt/verifyE8-LX1-c")
SRC = ROOT / "course/assets/data/market/fx_monthly.csv"
FILES = {
    "twin": ROOT / "tests/labs/LX1/lab-LX1-project-3.py",
    "mutant_blank_skipped": ROOT / "ledgers/LX1/mutants/lx1c_r8n03_lab3_blank_cell_skipped_silently.py",
    "mutant_gap_unchecked": ROOT / "ledgers/LX1/mutants/lx1c_r8n04_lab3_month_gap_not_checked.py",
}
rows = list(csv.reader(SRC.open(encoding="utf-8")))
hdr, body = rows[0], rows[1:]
gbp = hdr.index("GBP")
blank = [hdr] + [list(r) for r in body]
blank[301][gbp] = ""  # blank GBP cell in month 301 (1996-02 row index shifted by the header)
gap = [hdr] + [r for k, r in enumerate(body) if k != 300]  # one month removed in the middle
CASES = {"blank_cell": blank, "month_gap": gap}
for case, data in CASES.items():
    for name, path in FILES.items():
        with tempfile.TemporaryDirectory(prefix="lx1c-r8-raise-") as wd:
            pathlib.Path(wd, "data").mkdir()
            with open(pathlib.Path(wd, "data", "fx_monthly.csv"), "w", encoding="utf-8", newline="") as fh:
                csv.writer(fh).writerows(data)
            r = subprocess.run([sys.executable, "-I", "-W", "error", str(path)], cwd=wd, capture_output=True, text=True)
            last = r.stderr.strip().splitlines()[-1] if r.stderr.strip() else ""
            print(f"{case} | {name} | rc={r.returncode} | stdout_lines={len(r.stdout.splitlines())} | {last}")
