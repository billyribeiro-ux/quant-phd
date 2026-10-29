#!/bin/bash
# usage: run_alt.sh <solution.py> <seed>  -- grader workspace as tools/run_graders.py, verifier checkout
CO=/Users/billyribeiro/.fanout/wt/verifyB15-CS2-d
W=$(mktemp -d /tmp/cs2d15.XXXX)
cp "$CO/course/modules/CS/CS2/grader/test_project.py" "$CO/course/modules/CS/CS2/grader/instance.py" "$W/"
cp "$1" "$W/streamstats.py"
cd "$W" && out=$(env -i PATH=/usr/bin:/bin QF_SEED="$2" PYTHONHASHSEED=0 "$CO/.venv/bin/python" -I -W error -m pytest --assert=plain -W error -q -p no:cacheprovider test_project.py 2>&1)
rc=$?
echo "rc=$rc $(echo "$out" | tail -1)"
echo "$out" | grep -E "^FAILED" | head -2 | cut -c1-200
rm -rf "$W"
