#!/bin/bash
# Usage: grader_suite_r8.sh <solution.py> <seed> <workdir> [pytest args]
# Copies the M7 grader files (verifier checkout) and the given solution into <workdir>, then runs the suite there.
CK=/Users/billyribeiro/.fanout/wt/verifyD8-M7-d
SRC=$CK/course/modules/M/M7/grader
SOL=$1; SEED=$2; WD=$3; shift 3
rm -rf "$WD"; mkdir -p "$WD"
cp "$SRC/instance.py" "$SRC/test_project.py" "$WD/"
cp "$SOL" "$WD/constrained_allocator.py"
cd "$WD" && QF_SEED=$SEED $CK/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error "$@" test_project.py
