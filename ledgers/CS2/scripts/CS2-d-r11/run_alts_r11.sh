#!/bin/sh
# Run each alternative as streamstats.py against the current grader over seeds 0-49.
G=/Users/billyribeiro/.fanout/wt/verifyB11-CS2-d/course/modules/CS/CS2/grader
PY=/Users/billyribeiro/.fanout/wt/verifyB11-CS2-d/.venv/bin/python
for alt in "$1"/*.py; do
  W=$(mktemp -d /tmp/cs2r11alt.XXXX)
  cp "$G/test_project.py" "$G/instance.py" "$W/"
  cp "$alt" "$W/streamstats.py"
  pass=0; fail=0
  for s in $(seq 0 49); do
    if (cd "$W" && QF_SEED=$s "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); fi
  done
  echo "$(basename "$alt") seeds_pass=$pass seeds_fail=$fail"
  rm -rf "$W"
done
