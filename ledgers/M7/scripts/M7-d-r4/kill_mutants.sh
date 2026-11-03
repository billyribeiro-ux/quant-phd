#!/bin/bash
# Run one or more mutant files (args) against seeds 0-9 under the page's flags; print the first failing test per mutant.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD4-M7-d
G=$ROOT/course/modules/M/M7/grader
PY=$ROOT/.venv/bin/python
for mutant in "$@"; do
  name=$(basename $mutant .py)
  killed="SURVIVED"
  for seed in $(seq 0 9); do
    D=/tmp/m7d-r4-mut/$name/$seed
    rm -rf $D; mkdir -p $D
    cp $G/test_project.py $G/instance.py $D/
    cp $mutant $D/constrained_allocator.py
    out=$(cd $D && QF_SEED=$seed PYTHONHASHSEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
    if echo "$out" | grep -q " failed"; then
      t=$(echo "$out" | grep -E "^FAILED" | head -1 | sed 's/ - .*//')
      killed="KILLED seed $seed by $t"
      break
    fi
  done
  echo "$name: $killed"
done
