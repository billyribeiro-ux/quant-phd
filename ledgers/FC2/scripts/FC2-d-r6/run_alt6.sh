#!/bin/bash
# Round 6 FC2-d: the FC2 suite against alt6 (integer cross-multiplied alternative), seeds 0-49, and the 0-9 mutation window.
ROOT=/Users/billyribeiro/.fanout/wt/verifyC6-FC2-d
G=$ROOT/course/modules/FC/FC2/grader
PY=$ROOT/.venv/bin/python
S=$ROOT/ledgers/FC2/scripts/FC2-d-r6
W=$(mktemp -d /tmp/fc2d-r6-a6.XXXXXX)
cp "$G/test_project.py" "$G/instance.py" "$W/"; cp "$S/alt6_integer_crossmul.py" "$W/scanner.py"
fails=0
for s in $(seq 0 49); do
  out=$(cd "$W" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  case "$out" in *failed*) fails=$((fails+1)); echo "seed $s: $out";; *passed*) ;; *) echo "seed $s: ?? $out";; esac
done
echo "alt6 seeds 0-49: $fails seeds with failures"
rm -rf "$W"
