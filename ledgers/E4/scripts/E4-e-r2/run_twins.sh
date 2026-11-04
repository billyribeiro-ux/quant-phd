#!/bin/sh
# Slice e evidence (round 2): run every E4 lab twin in isolated mode with warnings as errors, one output block per lab.
# Usage (from the checkout root): sh ledgers/E4/scripts/E4-e-r2/run_twins.sh
set -e
for f in tests/labs/E4/lab-E4-L0*-1.py; do
  echo "== $f"
  .venv/bin/python -I -W error "$f"
done
