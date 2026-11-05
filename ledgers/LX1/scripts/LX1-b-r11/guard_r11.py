"""LX1-b round 11: fail-loud guard test of the L04 twin's loader (load_column, parse_rate, month_index).

The twin's module-level main() call is removed in memory, so only its functions run. Scratch CSVs go to a temp dir.
Usage: python -I ledgers/LX1/scripts/LX1-b-r11/guard_r11.py <checkout> <scratch-dir>
"""

import sys
from pathlib import Path

root = Path(sys.argv[1])
scratch = Path(sys.argv[2])
scratch.mkdir(parents=True, exist_ok=True)
src = (root / "tests/labs/LX1/lab-LX1-L04-1.py").read_text(encoding="utf-8")
src = src.rsplit("\nmain()", 1)[0]
ns: dict[str, object] = {"__name__": "twin_functions"}
exec(compile(src, "twin", "exec"), ns)
load_column = ns["load_column"]

cases = {
    "blank_cell": "month,GBP\n1971-01,2.4\n1971-02,\n",
    "nondecimal": "month,GBP\n1971-01,2.4\n1971-02,NA\n",
    "gap_month": "month,GBP\n1971-01,2.4\n1971-03,2.5\n",
    "missing_column": "month,EUR\n1971-01,2.4\n",
    "zero_rate": "month,GBP\n1971-01,2.4\n1971-02,0\n",
    "negative_sign": "month,GBP\n1971-01,2.4\n1971-02,-2.5\n",
    "exponent": "month,GBP\n1971-01,2.4\n1971-02,2.5e0\n",
    "bad_month": "month,GBP\n1971-13,2.4\n",
    "good": "month,GBP\n1971-01,2.4\n1971-02,2.5\n",
}
for name, body in cases.items():
    path = scratch / f"{name}.csv"
    path.write_text(body, encoding="utf-8")
    try:
        rows = load_column(path, "GBP")
        print(f"{name}: loaded {len(rows)} rows, first={rows[0]}")
    except ValueError as exc:
        print(f"{name}: ValueError: {exc}")
    except Exception as exc:  # report any other exception type too
        print(f"{name}: OTHER {type(exc).__name__}: {exc}")
