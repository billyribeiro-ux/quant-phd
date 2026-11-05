#!/bin/bash
# Round-10 verifier D: run every M4 alternative and the reference through the suite on seeds 0-9, in fresh scratch dirs.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD10-M4-d
PY=$ROOT/.venv/bin/python
G=$ROOT/course/modules/M/M4/grader
SCR=/tmp/d10_alts
files=("$G/reference.py"
  "$ROOT/ledgers/M4/scripts/M4-d-r10/alts/"*.py
  "$ROOT/ledgers/M4/scripts/M4-d-r9/alts/"alt_r9_*.py
  "$ROOT/ledgers/M4/scripts/M4-d-r8/alts/"alt*.py)
for f in "${files[@]}"; do
  pass=0; fail=""
  for s in 0 1 2 3 4 5 6 7 8 9; do
    d=$(mktemp -d "$SCR.XXXX")
    cp "$f" "$d/tail_risk.py"; cp "$G/instance.py" "$G/test_project.py" "$d/"
    out=$(cd "$d" && QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
    if echo "$out" | grep -q " failed\| error"; then fail="$fail seed$s[$out]"; else pass=$((pass+1)); fi
    rm -rf "$d"
  done
  echo "$(basename $(dirname $f))/$(basename $f): $pass/10 seeds pass${fail:+; FAIL:$fail}"
done
