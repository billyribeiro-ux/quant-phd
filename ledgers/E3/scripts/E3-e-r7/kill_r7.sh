#!/bin/bash
# Run each new r7 mutant as elicit.py against the suite on seeds 0-9; report the first failing test per seed.
PY=/Users/billyribeiro/.fanout/wt/verifyD7-E3-e/.venv/bin/python
G=/Users/billyribeiro/.fanout/wt/verifyD7-E3-e/course/modules/E/E3/grader
M=/Users/billyribeiro/.fanout/wt/verifyD7-E3-e/ledgers/E3/mutants
for m in "$M"/r7_0*.py; do
  name=$(basename "$m" .py)
  d=/tmp/e3e_r7/kill/$name; rm -rf "$d"; mkdir -p "$d"
  cp "$G/instance.py" "$G/test_project.py" "$d/"; cp "$m" "$d/elicit.py"
  for s in 0 1 2 3 4 5 6 7 8 9; do
    out=$(cd "$d" && QF_SEED=$s $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
    first=$(echo "$out" | grep -m1 "^FAILED\|Error\|failed" | cut -c1-200)
    echo "$name seed=$s : $(echo "$out" | tail -1 | cut -c1-120) | $(echo "$out" | grep -m1 '^FAILED' | cut -c1-160)"
  done
done
