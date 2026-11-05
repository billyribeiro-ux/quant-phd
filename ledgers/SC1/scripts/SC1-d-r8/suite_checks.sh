#!/bin/bash
# Round 8 (SC1-d): collect count, reference suite on seeds 0, 3, 7, starter on seed 0; scratch copy of the grader.
set -u
ROOT=/Users/billyribeiro/.fanout/wt/verifyE8-SC1-d
O=$ROOT/ledgers/SC1/scripts/SC1-d-r8/out
G=$ROOT/course/modules/SC/SC1/grader
PY=$ROOT/.venv/bin/python
W=$(mktemp -d /tmp/sc1d-r8-suite-XXXX)
cp "$G/test_project.py" "$G/instance.py" "$W"/
cp "$G/reference.py" "$W/bm_checks.py"
cd "$W" || exit 1
$PY -I -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -2 > "$O/collect_test_project_r8.txt"
for s in 0 3 7; do
  QF_SEED=$s $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 > "$O/suite_reference_seed${s}_r8.txt"
done
cp "$G/starter.py" "$W/bm_checks.py"
QF_SEED=0 $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1 > "$O/suite_starter_seed0_r8.txt"
cd / && rm -rf "$W"
echo done
