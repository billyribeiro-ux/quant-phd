#!/bin/bash
# Round 5 verifier script for FC2-d: collect-only count per seed on the reference, and starter failure.
G=/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/course/modules/FC/FC2/grader
PY=/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/.venv/bin/python
for s in $(seq 0 49); do
  W=$(mktemp -d /tmp/fc2d-r5-count.XXXXXX)
  cp "$G/test_project.py" "$G/instance.py" "$W/"
  cp "$G/reference.py" "$W/scanner.py"
  n=$(cd "$W" && QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error --collect-only test_project.py 2>/dev/null | tail -1)
  echo "seed $s collect: $n"
  rm -rf "$W"
done
W=$(mktemp -d /tmp/fc2d-r5-starter.XXXXXX)
cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$G/starter.py" "$W/scanner.py"
(cd "$W" && QF_SEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -2)
rm -rf "$W"
