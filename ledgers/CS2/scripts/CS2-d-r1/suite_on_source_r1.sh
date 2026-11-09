#!/bin/bash
# Usage: suite_on_source_r1.sh <library.py> <seeds...>; prints the last pytest line per seed (scratch dir, removed after)
ROOT=/Users/billyribeiro/.fanout/wt/verifyH1-CS2-d
SRC="$1"; shift
D=$(mktemp -d /tmp/cs2s.XXXXXX)
cp "$ROOT/course/modules/CS/CS2/grader/instance.py" "$ROOT/course/modules/CS/CS2/grader/test_project.py" "$D/"
cp "$SRC" "$D/streamstats.py"
cd "$D"
for s in "$@"; do
  echo "seed=$s $(QF_SEED=$s "$ROOT/.venv/bin/python" -m pytest test_project.py -q -p no:cacheprovider --assert=plain -W error 2>&1 | tail -1)"
done
rm -rf "$D"
