#!/bin/bash
# Round 6 (M7-d): run one alternative (arg 1) on one seed (arg 2) under the page's flags, in a scratch dir.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD6-M7-d
G=$ROOT/course/modules/M/M7/grader
PY=$ROOT/.venv/bin/python
alt=$1; seed=$2
name=$(basename "$alt" .py)
D=/tmp/m7d-r6-run/$name/$seed
rm -rf "$D"; mkdir -p "$D"
cp $G/test_project.py $G/instance.py "$D/"
cp "$alt" "$D/constrained_allocator.py"
res=$(cd "$D" && QF_SEED=$seed PYTHONDONTWRITEBYTECODE=1 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
echo "$name seed $seed: $res"
