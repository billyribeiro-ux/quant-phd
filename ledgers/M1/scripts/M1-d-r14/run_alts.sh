#!/bin/bash
# Runs every alternative correct implementation (rounds 10 to 14) against the fixed grader suite in a scratch workspace.
CK=/tmp/verify14-M1-d
PY=$CK/.venv/bin/python
G=$CK/course/modules/M/M1/grader
for f in $CK/ledgers/M1/scripts/M1-d-r1[0-4]/alt*.py $CK/ledgers/M1/scripts/M1-d-r1[0-4]/alts/alt*.py; do
  n=$(basename "$f" .py)
  w=$(mktemp -d /tmp/m1-v14/d/alt_XXXX)
  cp $G/test_project.py $G/instance.py "$w/"
  cp "$f" "$w/annuity_engine.py"
  res=$(cd "$w" && $PY -m pytest -q -W error -p no:cacheprovider test_project.py 2>&1 | tail -1)
  echo "$n :: $res"
done
