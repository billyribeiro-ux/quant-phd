#!/bin/sh
# Runs the E3 suite on each equivalent file for seeds 0-9. Usage (repo root): sh equivalent_seeds.sh <repo-root>
R="$1"
for f in "$R"/ledgers/E3/equivalent/*.py; do
  echo "== $(basename "$f")"
  sh "$R/ledgers/E3/scripts/E3-d-r14/run_suite_seeds.sh" "$R" "$f" 0 1 2 3 4 5 6 7 8 9
done
