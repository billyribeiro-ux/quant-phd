#!/bin/bash
# Local pytest of the grader suite in a scratch copy (outside the repo). Usage: local_suite_r16.sh <repo> <seed> <solution.py>
REPO="$1"; SEED="$2"; SOL="$3"
D=$(mktemp -d /tmp/pc3c_r16_run.XXXXXX)
G="$REPO/course/modules/PC/PC3/grader"
cp "$G/engine.py" "$G/instance.py" "$G/test_project.py" "$D/"
cp "$SOL" "$D/market_maker.py"
cd "$D" || exit 2
QF_SEED="$SEED" "$REPO/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error --collect-only test_project.py 2>&1 | tail -1
QF_SEED="$SEED" "$REPO/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -3
rm -rf "$D"
