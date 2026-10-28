#!/bin/bash
# Round 17: runs every alternative correct implementation (rounds 7 to 14) against the grader in the checkout.
CK=/tmp/verify17-M1-d
PY=$CK/.venv/bin/python
G=$CK/course/modules/M/M1/grader
for f in $(find $CK/ledgers/M1/scripts -name 'alt*.py' | sort); do
  n=$(basename "$f" .py)
  w=$(mktemp -d /tmp/m1-v17/d/alt_XXXX)
  cp $G/test_project.py $G/instance.py "$w/"
  cp "$f" "$w/annuity_engine.py"
  res=$(cd "$w" && QF_SEED=0 $PY -I -W error -m pytest -q -p no:cacheprovider --assert=plain test_project.py 2>&1 | tail -1)
  echo "$n :: $res"
done
