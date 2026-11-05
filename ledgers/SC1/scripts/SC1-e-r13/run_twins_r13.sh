#!/bin/sh
# Runs each SC1 lesson lab twin alone, in a scratch directory, under python -I -W error (no site path, warnings are errors).
# Usage: sh run_twins_r13.sh <checkout>
CO="$1"; PY="$CO/.venv/bin/python"; OUT="$CO/ledgers/SC1/scripts/SC1-e-r13/out"
for i in 01 02 03 04 05 06 07 08; do
  d=$(mktemp -d); cp "$CO/tests/labs/SC1/lab-SC1-L$i-1.py" "$d/"
  (cd "$d" && "$PY" -I -W error "lab-SC1-L$i-1.py" > "$OUT/twin_L$i.stdout" 2> "$OUT/twin_L$i.stderr"; echo "L$i exit $?")
  rm -rf "$d"
done
