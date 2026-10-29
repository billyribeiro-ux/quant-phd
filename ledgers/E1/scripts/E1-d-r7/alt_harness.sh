#!/bin/bash
# usage: alt_harness.sh <candidate.py> <label>  -> runs the E1 grader on seeds 0-49 against the candidate
PY=/Users/billyribeiro/.fanout/wt/verifyB7-E1-d/.venv/bin/python
G=/Users/billyribeiro/.fanout/wt/verifyB7-E1-d/course/modules/E/E1/grader
WS=/tmp/e1d-r7-alt-$2; rm -rf $WS; mkdir -p $WS; cp $G/test_project.py $G/instance.py $WS/; cp "$1" $WS/market_structure.py
cd $WS; pass=0; fail=0; first=""
for s in $(seq 0 49); do
  if QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1; then pass=$((pass+1)); else fail=$((fail+1)); [ -z "$first" ] && first=$(QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | grep -m1 "^FAILED" | cut -c1-160); fi
done
echo "$2: seeds passed=$pass failed=$fail first_failure=[$first]"
rm -rf $WS
