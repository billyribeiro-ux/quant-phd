#!/bin/bash
# usage: run_suite.sh IMPL.py SEEDS(e.g. 0-49) -> pytest result per seed in a fresh scratch dir (grader files copied)
IMPL=$1; A=${2%-*}; B=${2#*-}
G=/Users/billyribeiro/.fanout/wt/verifyC3-FC2-d/course/modules/FC/FC2/grader
PY=/Users/billyribeiro/.fanout/wt/verifyC3-FC2-d/.venv/bin/python
for s in $(seq $A $B); do
  D=$(mktemp -d /tmp/fc2d-r3.XXXXXX)
  cp "$G/test_project.py" "$G/instance.py" "$IMPL" "$D/" && cp "$IMPL" "$D/scanner.py"
  out=$(cd "$D" && QF_SEED=$s $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  echo "seed $s: $out"
  rm -rf "$D"
done
