#!/bin/bash
# Round-10: collect-only count of the E3 grader suite, run in a scratch copy with the reference engine as elicit.py.
set -e
REPO=/Users/billyribeiro/.fanout/wt/verifyD10-E3-e
W=$(mktemp -d /tmp/e3e_r10_collect.XXXX)
cp "$REPO/course/modules/E/E3/grader/reference.py" "$W/elicit.py"
cp "$REPO/course/modules/E/E3/grader/instance.py" "$REPO/course/modules/E/E3/grader/test_project.py" "$W/"
cd "$W"
"$REPO/.venv/bin/python" -m pytest --collect-only -q -p no:cacheprovider test_project.py | tail -n 2
rm -rf "$W"
