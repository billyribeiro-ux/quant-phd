#!/bin/bash
# usage: suite_scan_one.sh <seed> ; full suite with the reference as elicit.py, one seed, one line of output
seed="$1"
G=/Users/billyribeiro/.fanout/wt/verifyD12-E3-d/course/modules/E/E3/grader
res=$(TAILN=400 /Users/billyribeiro/.fanout/scratch/E3-d-r12/run_suite.sh "$G/reference.py" "$seed" "$G" 2>&1)
code=$(echo "$res" | grep '^EXIT=' | cut -d= -f2)
fails=$(echo "$res" | grep '^FAILED' | sed 's/ - .*//; s/FAILED test_project.py:://' | tr '\n' ' ')
echo "seed=$seed EXIT=$code $fails"
