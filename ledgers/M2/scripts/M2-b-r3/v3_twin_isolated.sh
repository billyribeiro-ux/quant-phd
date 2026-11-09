#!/bin/sh
# Run each slice lab twin alone, from a scratch copy directory, under python -I -W error.
# Usage: sh v3_twin_isolated.sh <repo_root> <outdir>
set -u
REPO="$1"; OUT="$2"
mkdir -p "$OUT"
for L in 07 08 09 10 11 12; do
  cp "$REPO/tests/labs/M2/lab-M2-L$L-1.py" "$OUT/lab-M2-L$L-1.py"
  ( cd "$OUT" && "$REPO/.venv/bin/python" -I -W error "lab-M2-L$L-1.py" > "$OUT/lab-M2-L$L-1.py.out" 2> "$OUT/lab-M2-L$L-1.py.err"; echo "L$L exit=$?" )
done
