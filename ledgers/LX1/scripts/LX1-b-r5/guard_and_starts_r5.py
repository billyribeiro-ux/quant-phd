"""Verifier round 5: (1) the L04 twin's guards raise on bad cells (run on scratch copies), and (2) the
window-two dispersion for other start months (the interpretation says a different start can change it).
Run with: python3 -I guard_and_starts_r5.py <checkout> <scratch_dir>
"""

from __future__ import annotations

import csv
import math
import subprocess
import sys
from decimal import Context, Decimal
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
twin = root / "tests/labs/LX1/lab-LX1-L04-1.py"
src = (root / "course/assets/data/market/fx_monthly.csv").read_text(encoding="utf-8").splitlines()
header = src[0].split(",")
gi = header.index("GBP")
cases = {
    "blank_gbp_cell": lambda cells: cells.__setitem__(gi, ""),
    "text_1.2.3": lambda cells: cells.__setitem__(gi, "1.2.3"),
    "exponent_1.5e2": lambda cells: cells.__setitem__(gi, "1.5e2"),
    "negative_-1.5": lambda cells: cells.__setitem__(gi, "-1.5"),
}
for name, mutate in cases.items():
    d = scratch / name / "data"
    d.mkdir(parents=True, exist_ok=True)
    lines = [src[0]]
    for k, line in enumerate(src[1:], start=1):
        cells = line.split(",")
        if k == 300:  # a mid-file row, inside window two as well as window one
            mutate(cells)
        lines.append(",".join(cells))
    (d / "fx_monthly.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
    r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], cwd=scratch / name, capture_output=True,
                       text=True)
    last = (r.stderr.strip().splitlines() or [""])[-1]
    print(f"{name}: exit {r.returncode}; last stderr line: {last}")

# a dropped (skipped) month: remove one row, so consecutive months do not follow
name = "skipped_month"
d = scratch / name / "data"
d.mkdir(parents=True, exist_ok=True)
lines = [src[0]] + [l for k, l in enumerate(src[1:], start=1) if k != 300]
(d / "fx_monthly.csv").write_text("\n".join(lines) + "\n", encoding="utf-8")
r = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], cwd=scratch / name, capture_output=True, text=True)
print(f"{name}: exit {r.returncode}; last stderr line: {(r.stderr.strip().splitlines() or [''])[-1]}")

# window-two dispersion for other starts (Decimal, 60 digits)
ctx = Context(prec=60)
rows = [(rec["month"], Decimal(rec["GBP"])) for rec in csv.DictReader(src)]
changes = [(b[0], ctx.ln(ctx.divide(b[1], a[1]))) for a, b in zip(rows, rows[1:])]


def sd(vals):
    n = len(vals)
    mean = sum(vals, Decimal(0)) / n
    return ctx.sqrt(sum(((v - mean) ** 2 for v in vals), Decimal(0)) / (n - 1))


for start in ("1990-01", "2000-01", "2010-01"):
    w = [c for m, c in changes if m >= start]
    print(f"window from {start}: n = {len(w)}, sd = {sd(w).quantize(Decimal('0.000001'))}")
