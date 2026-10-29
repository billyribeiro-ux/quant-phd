#!/bin/bash
# Round 5 FC2-d: run the FC2 suite against each alternative correct implementation for seeds 0-19.
S=/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/ledgers/FC2/scripts/FC2-d-r5
G=/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/course/modules/FC/FC2/grader
PY=/Users/billyribeiro/.fanout/wt/verifyC5-FC2-d/.venv/bin/python
for alt in "$S"/alts/*.py; do
  W=$(mktemp -d /tmp/fc2d-r5-alt.XXXXXX)
  cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$alt" "$W/scanner.py"
  res=""
  for s in $(seq 0 19); do
    out=$(cd "$W" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
    case "$out" in *failed*) res="$res seed$s:FAIL";; *passed*) ;; *) res="$res seed$s:?";; esac
  done
  echo "$(basename "$alt"): ${res:-all 20 seeds pass}"
  rm -rf "$W"
done
