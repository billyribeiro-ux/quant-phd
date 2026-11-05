#!/bin/bash
# Round-10 verifier: run the proposed-fix suite (scratch, not applied) on the reference, the five alternatives and the three new mutants, seeds 0-19.
R=/Users/billyribeiro/.fanout/wt/verifyD10-FC1-c
S=$R/ledgers/FC1/scripts/FC1-c-r10
run() { # $1 = solution file
  D=$(mktemp -d /tmp/fc1r10fix.XXXXXX)
  cp $S/proposed_fix_test_project_r10.py $D/test_project.py
  cp $R/course/modules/FC/FC1/grader/instance.py $D/
  cp "$1" $D/instruments.py
  pass=0; fail=0; failed=""
  for s in $(seq 0 19); do
    if (cd $D && QF_SEED=$s $R/.venv/bin/python -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > $D/log_$s.txt 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); failed="$failed $s"; fi
  done
  echo "$(basename $1): pass_seeds=$pass fail_seeds=$fail failed_seeds=[$failed ] last_line=$(tail -1 $D/log_0.txt)"
  rm -rf "$D"
}
for a in $R/ledgers/FC1/alternatives/a*.py; do run "$a"; done
run $R/course/modules/FC/FC1/grader/reference.py
for m in $R/ledgers/FC1/mutants/r10c_*.py; do run "$m"; done
