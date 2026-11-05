#!/bin/sh
# Collect-only count of the SC1 grader suite in a scratch copy with bm_checks.py = reference.py (the grader panel's layout).
set -e
REPO="$1"
W=$(mktemp -d /tmp/sc1d-r12-collect.XXXXXX)
G="$REPO/course/modules/SC/SC1/grader"
cp "$G/test_project.py" "$G/instance.py" "$W/"
cp "$G/reference.py" "$W/bm_checks.py"
cd "$W"
for s in 0 1 7 49; do
  QF_SEED=$s PYTHONHASHSEED=0 "$REPO/.venv/bin/python" -I -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -1
done
