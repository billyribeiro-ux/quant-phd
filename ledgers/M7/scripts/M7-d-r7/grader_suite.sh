#!/bin/bash
# Usage: grader_suite.sh <solution.py> <seed> <workdir> [pytest args]
# Copies the M7 grader files and the given solution into <workdir> (a scratch dir), then runs the suite there.
SRC=/Users/billyribeiro/.fanout/wt/verifyD7-M7-d/course/modules/M/M7/grader
SOL=$1; SEED=$2; WD=$3; shift 3
rm -rf "$WD"; mkdir -p "$WD"
cp "$SRC/instance.py" "$SRC/test_project.py" "$WD/"
cp "$SOL" "$WD/constrained_allocator.py"
cd "$WD" && QF_SEED=$SEED /Users/billyribeiro/.fanout/wt/verifyD7-M7-d/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error -p no:randomly "$@" test_project.py
