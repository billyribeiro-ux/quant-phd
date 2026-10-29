#!/bin/bash
# Runs the FC1 grader suite (test_project.py, instance.py from the checkout) against each alternative on seeds 0-49.
# Usage: bash ledgers/FC1/scripts/FC1-c-r2/run_alternatives.sh <checkout-root> <scratch-dir>
ROOT="$1"; S="$2"; PY="$ROOT/.venv/bin/python"
for f in "$ROOT"/ledgers/FC1/scripts/FC1-c-r2/alt/*.py; do
  n=$(basename "$f" .py); d="$S/$n"; rm -rf "$d"; mkdir -p "$d"
  cp "$ROOT/course/modules/FC/FC1/grader/instance.py" "$ROOT/course/modules/FC/FC1/grader/test_project.py" "$d/"
  cp "$f" "$d/instruments.py"
  fails=0
  for s in $(seq 0 49); do
    if ! (cd "$d" && QF_SEED=$s "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >"$d/out_$s.txt" 2>&1); then
      fails=$((fails+1)); [ $fails -le 2 ] && grep -m3 "FAILED\|Error" "$d/out_$s.txt" | sed "s/^/  seed $s: /"
    fi
  done
  echo "$n: seeds failing $fails of 50"
done
