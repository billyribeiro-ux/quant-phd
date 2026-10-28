#!/bin/bash
# usage: runalt.sh <module.py> ; runs the FC1 suite on seeds 0-49 against that file as instruments.py
PY=/tmp/verifyC1-FC1-c/.venv/bin/python
G=/tmp/verifyC1-FC1-c/course/modules/FC/FC1/grader
f="$1"; fail=0; pass=0; first=""
d=$(mktemp -d /tmp/fc1-v/c/work.XXXX)
cp "$f" "$d/instruments.py"; cp $G/test_project.py $G/instance.py "$d/"
for s in $(seq 0 49); do
  out=$(cd "$d" && QF_SEED=$s $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  if echo "$out" | grep -q failed; then fail=$((fail+1)); [ -z "$first" ] && first="seed $s: $out"; else pass=$((pass+1)); fi
done
echo "$(basename $f): seeds passed=$pass failed=$fail ${first}"
rm -rf "$d"
