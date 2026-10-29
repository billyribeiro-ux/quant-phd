#!/bin/bash
# usage: cand_seeds.sh <candidate.py> <first> <last> ; prints pass/fail counts over seeds and first failing tests
ALT="$1"; A=$2; B=$3
G=/tmp/verifyB5-CS2-d/course/modules/CS/CS2/grader
W=$(mktemp -d /tmp/CS2-v/d5/c.XXXX)
cp $G/instance.py $G/test_project.py "$W"/; cp "$ALT" "$W/streamstats.py"; cd "$W"
pass=0; fail=0; tests=""
for s in $(seq $A $B); do
  out=$(QF_SEED=$s /tmp/verifyB5-CS2-d/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
  if echo "$out" | tail -1 | grep -q " failed"; then fail=$((fail+1)); tests="$tests $(echo "$out" | grep FAILED | sed 's/FAILED test_project.py:://; s/ - .*//' | tr '\n' ',')@$s"; else pass=$((pass+1)); fi
done
echo "$(basename $ALT): pass $pass fail $fail"; echo "$tests" | tr ' ' '\n' | sed '/^$/d' | head -5
rm -rf "$W"
