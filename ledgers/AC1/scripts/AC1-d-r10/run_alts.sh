#!/bin/bash
# Usage: run_alts.sh <dir of candidate statements.py files>. Runs every candidate on seeds 0-9 (run mode).
for f in "$1"/*.py; do
  name=$(basename "$f" .py); bad=""
  for s in 0 1 2 3 4 5 6 7 8 9; do
    out=$(/tmp/verify10-AC1-d/ledgers/AC1/scripts/AC1-d-r10/run_suite.sh "$f" /tmp/AC1-v10/AC1-d/alt/$name/s$s $s run 2>&1)
    echo "$out" | grep -q "failed" && { bad="FAILED seed $s: $(echo "$out" | tail -1)"; break; }
    echo "$out" | grep -q " passed in" || { bad="ERROR seed $s: $(echo "$out" | tail -1)"; break; }
  done
  echo "$name: ${bad:-PASS seeds 0-9}"
done
