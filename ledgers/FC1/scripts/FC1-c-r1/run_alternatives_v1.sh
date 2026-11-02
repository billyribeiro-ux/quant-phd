#!/bin/sh
# Runs each alternative correct implementation (alt_v1/*.py) and the reference against the FC1 suite on seeds 0-19.
# Usage: run_alternatives_v1.sh <checkout-root>
ROOT="$1"
PY="$ROOT/.venv/bin/python"
GRADER="$ROOT/course/modules/FC/FC1/grader"
OUT="$(mktemp -d /tmp/fc1c_alt_XXXXXX)"
for impl in "$ROOT"/ledgers/FC1/scripts/FC1-c-r1/alt_v1/*.py "$GRADER/reference.py"; do
  name=$(basename "$impl" .py)
  fails=0
  for seed in $(seq 0 19); do
    work="$OUT/$name-$seed"
    mkdir -p "$work"
    cp "$GRADER/test_project.py" "$GRADER/instance.py" "$work/"
    cp "$impl" "$work/instruments.py"
    ( cd "$work" && QF_SEED=$seed "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$work/out.txt" 2>&1 ) || { fails=$((fails+1)); echo "FAIL $name seed $seed"; tail -3 "$work/out.txt"; }
  done
  echo "$name: failing seeds $fails of 20"
done
