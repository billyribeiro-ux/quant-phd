#!/bin/bash
# Collect-only count of the grader suite with the reference engine as elicit.py, in a scratch copy (repo copy untouched).
set -e
G=/Users/billyribeiro/.fanout/wt/verifyD7-E3-e/course/modules/E/E3/grader
D=$(mktemp -d /tmp/e3e_r7_collect.XXXX)
cp "$G/instance.py" "$G/test_project.py" "$G/reference.py" "$D/"
cp "$G/reference.py" "$D/elicit.py"
cd "$D" && /Users/billyribeiro/.fanout/wt/verifyD7-E3-e/.venv/bin/python -I -m pytest --collect-only -q -p no:cacheprovider test_project.py | tail -1
