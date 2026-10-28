#!/bin/bash
# usage: run_alt_r4.sh <solution.py> ; runs test_project.py on seeds 0-49 in fresh dirs
CHK=/tmp/verifyB4-M4-d
sol="$1"; pass=0; fail=0; failnames=""
for s in $(seq 0 49); do
  w=$(mktemp -d /tmp/M4-v/d/altwork.XXXX)
  cp $CHK/course/modules/M/M4/grader/test_project.py $CHK/course/modules/M/M4/grader/instance.py "$w"/
  cp "$sol" "$w/tail_risk.py"
  out=$(cd "$w" && QF_SEED=$s $CHK/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
  if echo "$out" | tail -1 | grep -q "failed"; then fail=$((fail+1)); failnames="$failnames $s:$(echo "$out" | grep -o 'FAILED [^ ]*' | head -2 | tr '\n' ' ')"; else pass=$((pass+1)); fi
  rm -rf "$w"
done
echo "$sol pass=$pass fail=$fail $failnames"
