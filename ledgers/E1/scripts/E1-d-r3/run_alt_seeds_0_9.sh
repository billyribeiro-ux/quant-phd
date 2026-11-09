#!/bin/bash
# Run each round-3 alternative against the grader on seeds 0-9 in a fresh scratch copy.
set -u
CHK="$1"
G="$CHK/course/modules/E/E1/grader"
PY="$CHK/.venv/bin/python"
for alt in "$CHK"/ledgers/E1/scripts/E1-d-r3/alternatives/*.py; do
  n=$(basename "$alt" .py)
  for seed in 0 1 2 3 4 5 6 7 8 9; do
    W=/tmp/e1d_r3/run_${n}_${seed}
    rm -rf "$W"; mkdir -p "$W"
    cp "$G/test_project.py" "$G/instance.py" "$W/"
    cp "$alt" "$W/market_structure.py"
    cd "$W" && QF_SEED=$seed "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > out.txt 2>&1
    rc=$?
    echo "$n seed=$seed exit=$rc $(tail -1 out.txt)"
  done
done
