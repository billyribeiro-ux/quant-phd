#!/bin/bash
# Re-runs every AC1 mutant in ledgers/AC1/mutants/ against the round-11 grader (seeds 0 and 17) and prints the
# first failing test for seed 0. Usage: run_mutants.sh <out dir>
set -u
OUT="$1"; S=/tmp/verify11-AC1-d/ledgers/AC1/scripts/AC1-d-r11/run_suite.sh; M=/tmp/verify11-AC1-d/ledgers/AC1/mutants
cd "$M" || exit 2
for f in m*.py; do
  n=${f%.py}
  a=$($S "$M/$f" "$OUT/mutall/$n/s0" 0 run)
  b=$($S "$M/$f" "$OUT/mutall/$n/s17" 17 run)
  first=$(cd "$OUT/mutall/$n/s0" && QF_SEED=0 /tmp/verify11-AC1-d/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py -rf 2>/dev/null | grep '^FAILED' | head -1 | sed 's/^FAILED //; s/ - .*//')
  echo "$n | seed0: $a | seed17: $b | first: $first"
done
