#!/bin/bash
# Usage: run_one_mutant.sh <mutant file> <out root>; prints one line: name | seed0: ... | seed17: ...
set -u
F="$1"; OUT="$2"; S=/tmp/verify19-AC1-d/ledgers/AC1/scripts/AC1-d-r19/run_suite.sh
n=$(basename "$F" .py)
a=$($S "$F" "$OUT/s0/$n" 0 run)
b=$($S "$F" "$OUT/s17/$n" 17 run)
echo "$n | seed0: $a | seed17: $b"
