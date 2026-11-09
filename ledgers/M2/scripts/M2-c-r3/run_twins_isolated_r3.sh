#!/bin/sh
# Run each L13-L18 lab twin alone under python -I -W error (verifier round 3). Usage: sh run_twins_isolated_r3.sh (from checkout root)
for n in 13 14 15 16 17 18; do
  echo "== L$n"
  .venv/bin/python -I -W error tests/labs/M2/lab-M2-L$n-1.py
  echo "exit=$?"
done
