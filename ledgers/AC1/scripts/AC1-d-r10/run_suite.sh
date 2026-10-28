#!/bin/bash
# Usage: run_suite.sh <candidate statements.py> <workdir> <seed> [collect]
# Copies grader/test_project.py and instance.py from the round-10 checkout into workdir, installs the candidate as
# statements.py, and runs the suite the way the browser does (warnings as errors, --assert=plain).
set -u
CAND="$1"; WD="$2"; SEED="$3"; MODE="${4:-run}"
CHK=/tmp/verify10-AC1-d
G=$CHK/course/modules/AC/AC1/grader
rm -rf "$WD"; mkdir -p "$WD"
cp "$G/test_project.py" "$G/instance.py" "$WD/"
cp "$CAND" "$WD/statements.py"
cd "$WD" || exit 2
if [ "$MODE" = "collect" ]; then
  QF_SEED="$SEED" $CHK/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error --collect-only test_project.py 2>&1 | tail -1
else
  QF_SEED="$SEED" $CHK/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -3
fi
