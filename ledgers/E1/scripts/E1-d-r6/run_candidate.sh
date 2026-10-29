#!/bin/bash
# Usage: run_candidate.sh <candidate market_structure.py> <seed> [pytest-extra...]
# Copies the E1 project grader (instance.py, test_project.py) and a candidate module into a fresh scratch dir,
# then runs the browser-equivalent pytest command from project.html section "Running the suite locally".
set -u
REPO=/Users/billyribeiro/.fanout/wt/verifyB6-E1-d
CAND="$1"; SEED="$2"; shift 2
WORK=$(mktemp -d /tmp/e1d-r6-XXXXXX)
cp "$REPO/course/modules/E/E1/grader/instance.py" "$REPO/course/modules/E/E1/grader/test_project.py" "$WORK/"
cp "$CAND" "$WORK/market_structure.py"
cd "$WORK" && QF_SEED="$SEED" "$REPO/.venv/bin/python" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py "$@" 2>&1
rc=$?
rm -rf "$WORK"
exit $rc
