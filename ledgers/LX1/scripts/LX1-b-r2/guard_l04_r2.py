"""Corrupt copies of fx_monthly.csv; the L04 twin must fail loud (non-zero exit, ValueError), never print numbers.

Usage: python -I guard_l04_r2.py <checkout> <scratch-dir>
"""
import csv
import io
import shutil
import subprocess
import sys
from pathlib import Path

checkout = Path(sys.argv[1])
scratch = Path(sys.argv[2])
src = checkout / "course/assets/data/market/fx_monthly.csv"
twin = checkout / "tests/labs/LX1/lab-LX1-L04-1.py"
text = src.read_text(encoding="utf-8")
rows = list(csv.reader(io.StringIO(text)))
header, body = rows[0], rows[1:]
gi = header.index("GBP")

def variant(name, data_rows, head=header):
    d = scratch / name
    if d.exists():
        shutil.rmtree(d)
    (d / "data").mkdir(parents=True)
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\n")
    w.writerow(head)
    w.writerows(data_rows)
    (d / "data" / "fx_monthly.csv").write_text(buf.getvalue(), encoding="utf-8")
    p = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], cwd=d, capture_output=True, text=True)
    last = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""
    print(f"{name}: exit={p.returncode} stdout_lines={len(p.stdout.splitlines())} last_stderr={last[:140]}")

# control: unmodified file must run
variant("control", body)
b = [list(r) for r in body]
b1 = [list(r) for r in body]; b1[300][gi] = ""; variant("blank_cell", b1)
b2 = [list(r) for r in body]; b2[300][gi] = "1.2.3"; variant("non_decimal", b2)
b3 = [list(r) for r in body]; del b3[300]; variant("month_gap", b3)
b4 = [list(r) for r in body]; b4[300][gi] = "0.0000"; variant("zero_rate", b4)
b5 = [list(r) for r in body]; b5[300][gi] = "-1.5"; variant("negative_rate", b5)
variant("missing_column", body, head=[h if h != "GBP" else "GBX" for h in header])
b6 = [list(r) for r in body]; b6[300][gi] = "1.5e2"; variant("exponent_cell", b6)
