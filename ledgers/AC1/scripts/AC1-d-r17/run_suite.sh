#!/bin/bash
# Usage: run_suite.sh <candidate statements.py> <workdir> <seed> [run|collect]
# Copies grader/test_project.py and instance.py from the round-17 checkout (pin fefbf8b) into workdir, installs the
# candidate as statements.py, and runs the suite with warnings as errors and --assert=plain.
set -u
CAND="$1"; WD="$2"; SEED="$3"; MODE="${4:-run}"
CHK=/tmp/verify17-AC1-d
G=$CHK/course/modules/AC/AC1/grader
rm -rf "$WD"; mkdir -p "$WD"
cp "$G/test_project.py" "$G/instance.py" "$WD/"
cp "$CAND" "$WD/statements.py"
cd "$WD" || exit 2
if [ "$MODE" = "collect" ]; then
  QF_SEED="$SEED" $CHK/.venv/bin/python -I -W error -m pytest -q -p no:cacheprovider --assert=plain --collect-only test_project.py 2>&1 | tail -1
else
  QF_SEED="$SEED" $CHK/.venv/bin/python -I -W error -m pytest -q -p no:cacheprovider --assert=plain test_project.py 2>&1 | tail -1
fi
