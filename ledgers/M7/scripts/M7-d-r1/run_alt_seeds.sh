#!/bin/bash
# Usage: run_alt_seeds.sh <solution.py> <first-seed> <last-seed>
# Runs the M7 suite (pytest flags of the browser) against one solution on each seed; prints one line per seed.
set -u
CHECKOUT="$(cd "$(dirname "$0")/../../../.." && pwd)"
G="$CHECKOUT/course/modules/M/M7/grader"
PY="$CHECKOUT/.venv/bin/python"
W=$(mktemp -d /tmp/m7d-run.XXXX)
cp "$G/test_project.py" "$G/instance.py" "$W/"
cp "$1" "$W/constrained_allocator.py"
cd "$W" || exit 1
for s in $(seq "$2" "$3"); do
  out=$(QF_SEED=$s PYTHONHASHSEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  echo "seed $s: $out"
done
rm -rf "$W"
