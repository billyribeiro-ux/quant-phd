#!/bin/bash
# usage: killers.sh <mutant.py> <seeds...>  -> prints distinct failing test names per seed
M="$1"; shift
W=$(mktemp -d /tmp/cs2d3/wk.XXXX)
cp /Users/billyribeiro/.fanout/wt/verifyD3-CS2-d/course/modules/CS/CS2/grader/test_project.py /Users/billyribeiro/.fanout/wt/verifyD3-CS2-d/course/modules/CS/CS2/grader/instance.py "$W/"
cp "$M" "$W/streamstats.py"
cd "$W"
for s in "$@"; do
  QF_SEED=$s /Users/billyribeiro/.fanout/wt/verifyD3-CS2-d/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | grep "^FAILED" | sed 's/ - .*//; s/^FAILED test_project.py:://' | sed "s/^/seed$s /"
done
rm -rf "$W"
