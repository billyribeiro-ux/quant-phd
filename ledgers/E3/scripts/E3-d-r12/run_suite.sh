#!/bin/bash
# usage: run_suite.sh <solution.py> <seed> <suite-dir-grader> ; prints pytest tail
set -u
SOL="$1"; SEED="$2"; GRADER="$3"
W=$(mktemp -d /Users/billyribeiro/.fanout/scratch/E3-d-r12/ws/run.XXXX)
cp "$GRADER/test_project.py" "$GRADER/instance.py" "$W/"
cp "$SOL" "$W/elicit.py"
cd "$W" && env -i PATH=/usr/bin:/bin:/opt/homebrew/bin QF_SEED="$SEED" PYTHONHASHSEED=0 /Users/billyribeiro/dev/quant-phd/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -${TAILN:-40}
echo "EXIT=${PIPESTATUS[0]}"
rm -rf "$W"
