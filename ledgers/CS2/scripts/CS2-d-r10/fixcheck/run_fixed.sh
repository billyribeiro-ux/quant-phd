#!/bin/sh
# usage: run_fixed.sh <solution.py> <seed>; runs the patched test copy against one solution in a temp workspace
W=$(mktemp -d /tmp/cs2d_fix_XXXX)
G=/Users/billyribeiro/.fanout/wt/verifyD10-CS2-d/course/modules/CS/CS2/grader
cp "$G/instance.py" "$W/"; cp "$1" "$W/streamstats.py"
cp /Users/billyribeiro/.fanout/wt/verifyD10-CS2-d/ledgers/CS2/scripts/CS2-d-r10/fixcheck/test_project_fixed.py "$W/test_project.py"
cd "$W" && QF_SEED=$2 /Users/billyribeiro/.fanout/wt/verifyD10-CS2-d/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1
rm -rf "$W"
