#!/bin/bash
# Usage: collect_counts_r1.sh <streamstats-source.py> <seeds>
# Copies grader files plus the given library into a fresh scratch dir and collects the suite per seed.
set -u
ROOT=/Users/billyribeiro/.fanout/wt/verifyH1-CS2-d
SRC="$1"; SEEDS="$2"
D=$(mktemp -d /tmp/cs2d.XXXXXX)
cp "$ROOT/course/modules/CS/CS2/grader/instance.py" "$ROOT/course/modules/CS/CS2/grader/test_project.py" "$D/"
cp "$SRC" "$D/streamstats.py"
cd "$D"
for s in $SEEDS; do
  out=$(QF_SEED=$s "$ROOT/.venv/bin/python" -m pytest test_project.py --collect-only -q -p no:cacheprovider 2>&1 | tail -1)
  echo "seed=$s $out"
done
rm -rf "$D"
