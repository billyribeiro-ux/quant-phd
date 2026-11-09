"""Round 21 (LX1-c): searches a synthetic series (window-two log changes scaled by f) for an input on which the
student error lx1c_r18n02 (difference from printed two-decimal sds) prints a different difference than the twin.
Test data only, not data. Usage: python -I diff_printed_search_r21.py <repo_root> <scratch>"""
import csv
import math
import subprocess
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
(scratch / "data").mkdir(parents=True, exist_ok=True)
src = list(csv.reader((root / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8", newline="")))
header, body = src[0], src[1:]
g = header.index("GBP")
rates = [float(r[g]) for r in body]
months = [r[0] for r in body]
changes = [math.log(rates[i] / rates[i - 1]) for i in range(1, len(rates))]


def build(f):
    out = [rates[0]]
    for i, c in enumerate(changes, start=1):
        m = months[i]
        c2 = c * f if m >= "2000-01" else c
        out.append(out[-1] * math.exp(c2))
    rows = []
    for r, v in zip(body, out):
        rr = list(r)
        rr[g] = f"{v:.10f}"
        rows.append(rr)
    with (scratch / "data" / "fx_monthly.csv").open("w", newline="", encoding="utf-8") as h:
        csv.writer(h).writerows([header] + rows)


def run(p):
    return subprocess.run([sys.executable, "-I", "-W", "error", str(p)], capture_output=True, text=True,
                          cwd=str(scratch), timeout=300).stdout


mutant = root / "ledgers/LX1/mutants/lx1c_r18n02_lab3_difference_of_printed_sds.py"
twin = root / "tests/labs/LX1/lab-LX1-project-3.py"
found = None
for f in [0.5 + 0.02 * k for k in range(0, 60)]:
    build(f)
    t, m = run(twin), run(mutant)
    if t != m:
        found = f
        print(f"f={f:.2f}: twin and mutant differ")
        print("".join(a for a in t.splitlines(True) if "difference" in a), end="")
        print("".join(a for a in m.splitlines(True) if "difference" in a), end="")
        break
    print(f"f={f:.2f}: same")
print("found", found)
