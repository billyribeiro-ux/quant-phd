#!/bin/bash
# Re-runs every AC1 mutant in ledgers/AC1/mutants/ against the round-17 grader (seeds 0 and 17).
# Usage: run_mutants.sh <out dir> <mutant dir>
set -u
OUT="$1"; M="$2"; S=/tmp/verify17-AC1-d/ledgers/AC1/scripts/AC1-d-r17/run_suite.sh
cd "$M" || exit 2
for f in *.py; do
  n=${f%.py}
  a=$($S "$M/$f" "$OUT/s0/$n" 0 run)
  b=$($S "$M/$f" "$OUT/s17/$n" 17 run)
  echo "$n | seed0: $a | seed17: $b"
done
