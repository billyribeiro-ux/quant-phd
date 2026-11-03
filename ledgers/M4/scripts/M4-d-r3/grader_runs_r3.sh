#!/bin/bash
# Round-3 verifier D: run the M4 autograder suite with the reference solution (and a seeded instance) in a scratch copy.
# Usage: grader_runs_r3.sh <checkout_root> <solution.py> <seed>   (prints collect-only count and the pytest tail)
ROOT=$1; SOL=$2; SEED=$3
SCR=$(mktemp -d /tmp/m4d_r3_grader.XXXXXX)
cp "$ROOT/course/modules/M/M4/grader/test_project.py" "$ROOT/course/modules/M/M4/grader/instance.py" "$SCR/"
cp "$SOL" "$SCR/tail_risk.py"
cd "$SCR" || exit 1
QF_SEED=$SEED "$ROOT/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -3
echo "EXIT_PYTEST=${PIPESTATUS[0]}"
echo "collect_only_count: $(QF_SEED=$SEED "$ROOT/.venv/bin/python" -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>/dev/null | tail -1)"
rm -rf "$SCR"
