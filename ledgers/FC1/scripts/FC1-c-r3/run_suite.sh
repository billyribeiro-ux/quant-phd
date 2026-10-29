#!/bin/bash
# Usage: run_suite.sh <checkout-root> <solution.py> <scratch-dir> <seed-from> <seed-to>
# Copies the FC1 grader (instance.py, test_project.py) and the given solution into a scratch dir as instruments.py,
# then runs pytest with the browser flags for each seed. Prints the number of failing seeds.
ROOT="$1"; SOL="$2"; D="$3"; A="${4:-0}"; B="${5:-49}"; PY="$ROOT/.venv/bin/python"
rm -rf "$D"; mkdir -p "$D"
cp "$ROOT/course/modules/FC/FC1/grader/instance.py" "$ROOT/course/modules/FC/FC1/grader/test_project.py" "$D/"
cp "$SOL" "$D/instruments.py"
fails=0; first=""
for s in $(seq "$A" "$B"); do
  if ! (cd "$D" && QF_SEED=$s "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >"$D/out_$s.txt" 2>&1); then
    fails=$((fails+1)); [ -z "$first" ] && first="seed $s: $(grep -m1 -E '^E |FAILED|Failed' "$D/out_$s.txt" | head -1)"
  fi
done
echo "$(basename "$SOL"): failing seeds $fails of $((B-A+1)) ${first:+| first: $first}"
