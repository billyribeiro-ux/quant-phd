#!/bin/sh
# Run each alternative as streamstats.py against the r12 checkout grader over seeds 0-49.
CK=/Users/billyribeiro/.fanout/wt/verifyB12-CS2-d
G=$CK/course/modules/CS/CS2/grader
PY=$CK/.venv/bin/python
for alt in "$1"/*.py; do
  W=$(mktemp -d /tmp/cs2r12alt.XXXX)
  cp "$G/test_project.py" "$G/instance.py" "$W/"
  cp "$alt" "$W/streamstats.py"
  pass=0; fail=0
  for s in $(seq 0 49); do
    if (cd "$W" && QF_SEED=$s PYTHONHASHSEED=0 "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); fi
  done
  echo "$(basename "$alt") seeds_pass=$pass seeds_fail=$fail"
  rm -rf "$W"
done
