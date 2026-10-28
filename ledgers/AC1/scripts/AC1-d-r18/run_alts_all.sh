#!/bin/bash
# Runs every alternative implementation found under ledgers/AC1/scripts/*/alts* (excluding the round-17 copies
# already in this folder) against the round-18 grader on seeds 0-49. Prints one line per alternative.
set -u
ROOT=/tmp/verify18-AC1-d/ledgers/AC1/scripts
S=/tmp/verify18-AC1-d/ledgers/AC1/scripts/AC1-d-r18/run_suite.sh
OUT=/tmp/ac1-v/d18/altsall
for f in $(find "$ROOT" -path "*alts*" -name "alt_*.py" ! -path "*AC1-d-r18*" | sort); do
  n=$(basename "$f" .py)
  bad=0
  for s in $(seq 0 49); do
    r=$($S "$f" "$OUT/$n/s$s" "$s" run)
    case "$r" in *" failed"*|"") bad=$((bad+1)); echo "  $n seed $s: $r";; esac
  done
  echo "$n: seeds with failures: $bad of 50"
done
echo ALTS_DONE
