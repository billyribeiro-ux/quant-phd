#!/bin/bash
# usage: run_mutant_seeds.sh <mutant.py> <seed-list-space-separated>
# copies the grader and the mutant into a fresh scratch dir and runs the suite once per seed
PY=/Users/billyribeiro/.fanout/wt/verifyB10-M4-d/.venv/bin/python
GRADER=/Users/billyribeiro/.fanout/wt/verifyB10-M4-d/course/modules/M/M4/grader
MUT="$1"; shift
W=$(mktemp -d /tmp/M4-d-r10-mut.XXXXXX)
cp "$GRADER/test_project.py" "$GRADER/instance.py" "$W/"
cp "$MUT" "$W/tail_risk.py"
cd "$W"
for s in "$@"; do
  out=$(QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
  echo "seed $s: $out"
done
rm -rf "$W"
