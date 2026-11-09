#!/bin/bash
# Round 18: collect-only count of the E4 project suite with reference.py installed as solver.py (the suite imports solver
# by name). Work happens in a fresh scratch copy; the checkout is not modified.
set -u
ROOT=/Users/billyribeiro/.fanout/wt/verifyE18-E4-d
SRC="$ROOT/course/modules/E/E4/grader"
S=$(mktemp -d /Users/billyribeiro/.fanout/scratch-E4-d-r18/collect.XXXX)
cp "$SRC/test_project.py" "$SRC/instance.py" "$S/" && cp "$SRC/reference.py" "$S/solver.py"
cd "$S" && QF_SEED=0 "$ROOT/.venv/bin/python" -I -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1
echo "exit $?"
