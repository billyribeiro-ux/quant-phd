"""Fail-loud guard check for the L04 twin: mutated scratch CSVs must make the twin exit nonzero.

Usage: python3 -I guard_L04.py <checkout> <scratch-dir>
"""
import csv
import subprocess
import sys
from pathlib import Path

checkout, scratch = Path(sys.argv[1]), Path(sys.argv[2])
src = checkout / "course/assets/data/market/fx_monthly.csv"
twin = checkout / "tests/labs/LX1/lab-LX1-L04-1.py"
with src.open(encoding="utf-8", newline="") as h:
    rows = list(csv.reader(h))
header, body = rows[0], rows[1:]
gi = header.index("GBP")
cases = {
    "blank_gbp_1995_12": lambda b: [r[:gi] + [""] + r[gi + 1:] if r[0] == "1995-12" else r for r in b],
    "exponent_cell": lambda b: [r[:gi] + ["1.5e2"] + r[gi + 1:] if r[0] == "1995-12" else r for r in b],
    "skipped_month": lambda b: [r for r in b if r[0] != "1996-01"],
    "no_gbp_column": None,
    "unchanged_file": lambda b: b,
}
for name, fn in cases.items():
    d = scratch / name / "data"
    d.mkdir(parents=True, exist_ok=True)
    out = d / "fx_monthly.csv"
    with out.open("w", encoding="utf-8", newline="") as h:
        w = csv.writer(h)
        if fn is None:
            hdr = [c if c != "GBP" else "GBP_X" for c in header]
            w.writerow(hdr)
            w.writerows(body)
        else:
            w.writerow(header)
            w.writerows(fn(body))
    p = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], cwd=scratch / name,
                       capture_output=True, text=True, check=False)
    last = (p.stderr.strip().splitlines() or [""])[-1]
    print(f"{name}: exit {p.returncode}; stderr last line: {last}")
