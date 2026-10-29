#!/bin/bash
# Usage: run_alt_one.sh <alt file> <out root>; runs one alternative on seeds 0-49, prints failing seed count.
set -u
F="$1"; OUT="$2"; S=/tmp/verify22-AC1-d/ledgers/AC1/scripts/AC1-d-r22/run_suite.sh
n=$(basename "$F" .py)
bad=0; for s in $(seq 0 49); do
  r=$($S "$F" "$OUT/$n/s$s" "$s" run)
  case "$r" in *" failed"*|"") bad=$((bad+1)); echo "  $n seed $s: $r";; esac
done
echo "$n: seeds with failures: $bad of 50"
