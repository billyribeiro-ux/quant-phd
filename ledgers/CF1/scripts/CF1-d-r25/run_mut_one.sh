#!/bin/bash
# Run one mutant (arg1) against the CF1 suite on seeds 0-9; print KILLED/SURVIVED with the first failing test.
CHK=/tmp/verify25-CF1-d
G=$CHK/course/modules/CF/CF1/grader
PY=$CHK/.venv/bin/python
M=$1
W=$(mktemp -d /tmp/CF1-v/d25/mut.XXXX)
cp $G/test_project.py $G/instance.py $W/ && cp "$M" $W/capbudget.py
for s in 0 1 2 3 4 5 6 7 8 9; do
  out=$(cd $W && QF_SEED=$s PYTHONHASHSEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
  if [ $? -ne 0 ]; then echo "KILLED $(basename $M) seed $s: $(echo "$out" | grep '^FAILED' | head -1 | cut -c1-160)"; rm -rf $W; exit 0; fi
done
echo "SURVIVED $(basename $M) (seeds 0-9)"; rm -rf $W
