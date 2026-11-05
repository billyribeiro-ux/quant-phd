#!/bin/bash
# Round-10 verifier D: run the M4 autograder (grader/test_project.py) on the reference, the starter, and seeds 0 and 3, in fresh
# scratch directories copied from the checkout's grader folder. Prints the collect count and each run's last line and exit code.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD10-M4-d
G=$ROOT/course/modules/M/M4/grader
PY=$ROOT/.venv/bin/python
run_in() {  # $1 = label, $2 = solution file, $3 = seed
  d=$(mktemp -d /tmp/d10_suite.XXXX)
  cp "$2" "$d/tail_risk.py"; cp "$G/instance.py" "$G/test_project.py" "$d/"
  out=$(cd "$d" && QF_SEED=$3 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
  rc=$?
  echo "$1 seed=$3 exit=$rc last: $(echo "$out" | grep -E 'passed|failed' | tail -1)"
  rm -rf "$d"
}
d=$(mktemp -d /tmp/d10_collect.XXXX); cp "$G/reference.py" "$d/tail_risk.py"; cp "$G/instance.py" "$G/test_project.py" "$d/"
echo "collect: $(cd "$d" && $PY -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -1)"; rm -rf "$d"
run_in reference "$G/reference.py" 0
run_in reference "$G/reference.py" 3
run_in starter "$G/starter.py" 0
run_in starter "$G/starter.py" 1
