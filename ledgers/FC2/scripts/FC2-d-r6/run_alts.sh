#!/bin/bash
# Round 6 FC2-d: run the FC2 suite (round-6 checkout) against each alternative correct implementation, seeds 0-19.
ROOT=/Users/billyribeiro/.fanout/wt/verifyC6-FC2-d
S=$ROOT/ledgers/FC2/scripts/FC2-d-r5
G=$ROOT/course/modules/FC/FC2/grader
PY=$ROOT/.venv/bin/python
for alt in "$S"/alts/*.py; do
  W=$(mktemp -d /tmp/fc2d-r6-alt.XXXXXX)
  cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$alt" "$W/scanner.py"
  res=""
  for s in $(seq 0 19); do
    out=$(cd "$W" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
    case "$out" in *failed*) res="$res seed$s:FAIL";; *passed*) ;; *) res="$res seed$s:?";; esac
  done
  echo "$(basename "$alt"): ${res:-all 20 seeds pass}"
  rm -rf "$W"
done
