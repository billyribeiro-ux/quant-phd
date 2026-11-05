#!/bin/sh
# Loader guards of the L04 twin on malformed CSVs (LX1-b r7). Run from the checkout root.
set -e
CK=$(pwd)
G=/tmp/lx1b-r7/guard; rm -rf "$G"; mkdir -p "$G"
sed '$d' "$CK/tests/labs/LX1/lab-LX1-L04-1.py" > "$G/guard_mod.py"
printf 'month,GBP\n2000-01,1.5\n2000-02,\n' > "$G/blank.csv"
printf 'month,GBP\n2000-01,1.5\n2000-03,1.6\n' > "$G/gap.csv"
printf 'month,USD\n2000-01,1.5\n' > "$G/nocol.csv"
printf 'month,GBP\n2000-01,1.5\n2000-02,1.5\n2000-03,1.5e0\n' > "$G/exp.csv"
cat > "$G/run_guard.py" <<'PY'
import sys
sys.path.insert(0, sys.argv[1])
from pathlib import Path
import guard_mod as g
for name in ("blank.csv", "gap.csv", "nocol.csv", "exp.csv"):
    try:
        rows = g.load_column(Path(sys.argv[1]) / name, "GBP")
        print(name, "LOADED", len(rows))
    except ValueError as e:
        print(name, "ValueError:", e)
PY
cd "$G" && "$CK/.venv/bin/python" -I -W error "$G/run_guard.py" "$G"
