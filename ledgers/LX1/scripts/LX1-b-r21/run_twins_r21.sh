#!/bin/bash
# Run each LX1 lab twin alone under python -I -W error from an empty scratch directory.
set -u
R="$1"
O="$R/ledgers/LX1/scripts/LX1-b-r21/out"
PY="$R/.venv/bin/python"
for L in L01 L03 L04; do
  S="/tmp/lx1b-r21-$L"
  rm -rf "$S"; mkdir -p "$S"
  if [ "$L" = "L04" ]; then mkdir -p "$S/data"; cp "$R/course/assets/data/market/fx_monthly.csv" "$S/data/"; fi
  (cd "$S" && "$PY" -I -W error "$R/tests/labs/LX1/lab-LX1-$L-1.py" > "$O/twin_$L.out" 2> "$O/twin_$L.err"; echo "exit $?" >> "$O/twin_$L.out")
  rm -rf "$S"
done
