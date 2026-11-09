#!/bin/sh
# Collect-only count of the M7 project suite for a seed, run in a scratch copy of the grader files.
set -e
SEED="$1"
REPO="$2"
W=$(mktemp -d /tmp/m7d-collect-XXXX)
cp "$REPO/course/modules/M/M7/grader/test_project.py" "$REPO/course/modules/M/M7/grader/instance.py" "$W/"
cp "$REPO/course/modules/M/M7/grader/reference.py" "$W/constrained_allocator.py"
cd "$W"
QF_SEED="$SEED" "$REPO/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error --collect-only test_project.py 2>&1 | tail -3
rm -rf "$W"
