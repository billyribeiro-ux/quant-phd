#!/bin/bash
# usage: run_one.sh <solution.py> <seed>
W=$(mktemp -d /tmp/cs2d14.XXXX)
/Users/billyribeiro/.fanout/wt/verifyB14-CS2-d/ledgers/CS2/scripts/CS2-d-r14/mkws.sh "$1" "$W"
cd "$W" && out=$(env -i PATH=/usr/bin:/bin QF_SEED="$2" PYTHONHASHSEED=0 /Users/billyribeiro/.fanout/wt/verifyB14-CS2-d/.venv/bin/python -I -W error -m pytest --assert=plain -W error -q -p no:cacheprovider test_project.py 2>&1)
rc=$?
echo "rc=$rc $(echo "$out" | tail -1)"
echo "$out" | grep -E "^FAILED" | head -1 | cut -c1-200
