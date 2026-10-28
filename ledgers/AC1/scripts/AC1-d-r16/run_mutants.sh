#!/bin/bash
# Re-runs every AC1 mutant in ledgers/AC1/mutants/ against the round-16 grader (seeds 0 and 17) and prints the first
# failing test for seed 0. Usage: run_mutants.sh <out dir> <mutant dir> [glob]
set -u
OUT="$1"; M="$2"; GLOB="${3:-*.py}"; S=/tmp/verify16-AC1-d/ledgers/AC1/scripts/AC1-d-r16/run_suite.sh
cd "$M" || exit 2
for f in $GLOB; do
  n=${f%.py}
  a=$($S "$M/$f" "$OUT/mutall/$n/s0" 0 run)
  b=$($S "$M/$f" "$OUT/mutall/$n/s17" 17 run)
  echo "$n | seed0: $a | seed17: $b"
done
