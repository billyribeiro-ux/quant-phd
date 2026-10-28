#!/bin/bash
# usage: run_alt.sh <alt.py> <seeds...>; runs the suite against one candidate file
ALT="$1"; shift
G=/tmp/verifyB5-CS2-d/course/modules/CS/CS2/grader
W=$(mktemp -d /tmp/CS2-v/d5/w.XXXX)
cp $G/instance.py $G/test_project.py "$W"/
cp "$ALT" "$W/streamstats.py"
cd "$W"
for s in "$@"; do
  echo "seed $s: $(QF_SEED=$s /tmp/verifyB5-CS2-d/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)"
  QF_SEED=$s /tmp/verifyB5-CS2-d/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | grep FAILED | head -3
done
rm -rf "$W"
