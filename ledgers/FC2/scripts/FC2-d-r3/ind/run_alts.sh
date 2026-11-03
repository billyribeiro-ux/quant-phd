#!/bin/bash
# Runs every alternative (archived in alts/) as scanner.py against the CURRENT grader test_project.py and instance.py,
# seeds 0..49, in a scratch dir under /tmp (never in the checkout). Prints per-alt pass/fail seed counts.
CHECKOUT="$1"
GRADER="$CHECKOUT/course/modules/FC/FC2/grader"
ALTS="$CHECKOUT/ledgers/FC2/scripts/FC2-d-r3/ind/alts"
PY="$CHECKOUT/.venv/bin/python"
for alt in "$ALTS"/alt_*.py; do
  name=$(basename "$alt" .py)
  pass=0; fail=0; failnames=""
  for seed in $(seq 0 49); do
    work=/tmp/fc2d-r3-ind/$name/s$seed
    rm -rf "$work"; mkdir -p "$work"
    cp "$GRADER/test_project.py" "$GRADER/instance.py" "$work/"
    cp "$alt" "$work/scanner.py"
    if (cd "$work" && QF_SEED=$seed "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > out.txt 2>&1); then
      pass=$((pass+1))
    else
      fail=$((fail+1)); failnames="$failnames $(cd "$work" && grep -o 'FAILED [^ ]*' out.txt | sed 's/FAILED test_project.py::/ /' | awk '{print $1}' | sort | uniq -c | tr -s ' ' | tr '\n' ';')"
    fi
  done
  echo "$name: pass seeds=$pass fail seeds=$fail"
  echo "   failing tests (per-seed tally): $(echo $failnames | tr -s ' ' | cut -c1-600)"
done
