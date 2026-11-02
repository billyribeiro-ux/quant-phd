#!/bin/bash
# Round-1 E3-d: run each new mutant against test_project.py on seeds 0-9 (same flags as the browser).
ROOT=/Users/billyribeiro/.fanout/wt/verifyD1-E3-d
PY=$ROOT/.venv/bin/python
for m in "$ROOT"/ledgers/E3/mutants/e3d1_*.py; do
  name=$(basename "$m" .py)
  for seed in 0 1 2 3 4 5 6 7 8 9; do
    W=$(mktemp -d /tmp/e3d_r1/mut_XXXX)
    cp "$ROOT/course/modules/E/E3/grader/test_project.py" "$ROOT/course/modules/E/E3/grader/instance.py" "$m" "$W/"
    mv "$W/$(basename "$m")" "$W/elicit.py"
    out=$(cd "$W" && QF_SEED=$seed $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
    rc=$?
    rm -rf "$W"
    if [ $rc -ne 0 ]; then
      echo "KILLED $name seed=$seed: $(echo "$out" | grep -E '^FAILED' | head -1)"
      break
    fi
    [ $seed -eq 9 ] && echo "SURVIVED $name on seeds 0-9"
  done
done
