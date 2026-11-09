#!/bin/bash
# PC3 slice c, round 1. mypy --strict on the grader with reference.py as market_maker.py, in a scratch copy.
REPO=/Users/billyribeiro/.fanout/wt/verifyF31-PC3-c
G="$REPO/course/modules/PC/PC3/grader"
D=$(mktemp -d /tmp/pc3c_r1_mypy.XXXXXX)
cp "$G/engine.py" "$G/instance.py" "$G/test_project.py" "$D/"
cp "$G/reference.py" "$D/market_maker.py"
cd "$D" && "$REPO/.venv/bin/mypy" --strict --no-incremental --cache-dir "$D/.mypy_cache" engine.py instance.py market_maker.py test_project.py
echo "EXIT=$?"
rm -rf "$D"
