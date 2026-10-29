#!/bin/bash
# Round 6 FC2-d: collect-only count per seed on the reference (seeds 0-49), and starter failure.
ROOT=/Users/billyribeiro/.fanout/wt/verifyC6-FC2-d
G=$ROOT/course/modules/FC/FC2/grader
PY=$ROOT/.venv/bin/python
for s in $(seq 0 49); do
  W=$(mktemp -d /tmp/fc2d-r6-count.XXXXXX)
  cp "$G/test_project.py" "$G/instance.py" "$W/"
  cp "$G/reference.py" "$W/scanner.py"
  n=$(cd "$W" && QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error --collect-only test_project.py 2>/dev/null | tail -1)
  echo "seed $s collect: $n"
  rm -rf "$W"
done
W=$(mktemp -d /tmp/fc2d-r6-starter.XXXXXX)
cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$G/starter.py" "$W/scanner.py"
(cd "$W" && QF_SEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -2)
rm -rf "$W"
