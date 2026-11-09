#!/bin/sh
# Round-12 verifier (M3 slice d): run one mutant module against the M3 suite on seeds 0-9 under the browser flags.
# Usage (from the checkout root): sh run_one_mutant_r12.sh <path-to-mutant.py>
ROOT="$(pwd)"
PY="$ROOT/.venv/bin/python"
G="$ROOT/course/modules/M/M3/grader"
name=$(basename "$1" .py)
d="/private/tmp/verifyD12-M3-mut/$name"
rm -rf "$d"; mkdir -p "$d"
cp "$G/instance.py" "$G/test_project.py" "$d/"
cp "$1" "$d/covariance_doctor.py"
for s in 0 1 2 3 4 5 6 7 8 9; do
  if (cd "$d" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$d/seed$s.out" 2>&1); then
    echo "$name seed $s: all passed"
  else
    echo "$name seed $s: FAILED: $(grep '^FAILED' "$d/seed$s.out" | sed 's/ - .*//' | head -3 | tr '\n' ' ')"
  fi
done
