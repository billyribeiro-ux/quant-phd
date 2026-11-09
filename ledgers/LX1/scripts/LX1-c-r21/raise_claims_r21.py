"""Round 21 (LX1-c): tests the project lab 3 'Check' claims (docstring lines 308-309 and the twin's ValueError
behaviour) on synthetic edits of a copy of fx_monthly.csv. Test data only, not data.
Usage: python -I raise_claims_r21.py <repo_root> <scratch>"""
import csv
import subprocess
import sys
from pathlib import Path

root, scratch = Path(sys.argv[1]), Path(sys.argv[2])
(scratch / "data").mkdir(parents=True, exist_ok=True)
src = list(csv.reader((root / "course/assets/data/market/fx_monthly.csv").open(encoding="utf-8", newline="")))
header, body = src[0], src[1:]
g = header.index("GBP")
twin = root / "tests/labs/LX1/lab-LX1-project-3.py"


def case(name, edit):
    rows = [list(r) for r in body]
    edit(rows)
    with (scratch / "data" / "fx_monthly.csv").open("w", newline="", encoding="utf-8") as h:
        csv.writer(h).writerows([header] + rows)
    p = subprocess.run([sys.executable, "-I", "-W", "error", str(twin)], capture_output=True, text=True,
                       cwd=str(scratch), timeout=120)
    last = p.stderr.strip().splitlines()[-1] if p.stderr.strip() else ""
    raised = p.returncode != 0 and last.startswith("ValueError")
    print(f"{name}: rc={p.returncode} ValueError={raised} :: {last}")


case("unedited snapshot", lambda rows: None)
case("blank GBP cell", lambda rows: rows[100].__setitem__(g, ""))
case("non-decimal GBP cell (exponent)", lambda rows: rows[100].__setitem__(g, "1.2e-1"))
case("text GBP cell", lambda rows: rows[100].__setitem__(g, "abc"))
case("negative GBP cell", lambda rows: rows[100].__setitem__(g, "-1.5"))
case("space-padded GBP cell", lambda rows: rows[100].__setitem__(g, " 1.5"))
case("month deleted (gap)", lambda rows: rows.pop(100))
case("duplicate month", lambda rows: rows[101].__setitem__(0, rows[100][0]))
