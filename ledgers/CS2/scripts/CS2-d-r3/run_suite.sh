#!/bin/bash
# usage: run_suite.sh <streamstats.py path> <seed-list>
SRC="$1"; SEEDS="$2"; PY=/Users/billyribeiro/.fanout/wt/verifyD3-CS2-d/.venv/bin/python
G=/Users/billyribeiro/.fanout/wt/verifyD3-CS2-d/course/modules/CS/CS2/grader
W=$(mktemp -d /tmp/cs2d3/work.XXXXXX)
cp "$G/test_project.py" "$G/instance.py" "$W/"
cp "$SRC" "$W/streamstats.py"
cd "$W"
res=PASS
for s in $SEEDS; do
  out=$(QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
  rc=$?
  if [ $rc -ne 0 ]; then res="KILLED(seed $s): $(echo "$out" | grep -m1 -o 'FAILED [^ ]*' )"; break; fi
  last=$(echo "$out" | tail -1)
done
echo "$(basename "$SRC"): $res"
rm -rf "$W"
