#!/bin/bash
# Round-1 M2-e verifier: grader suite staged the way tools/run_graders.py stages it (suite, support file, solution as sensitivity_engine.py).
R=/Users/billyribeiro/.fanout/wt/verifyG1-M2-e
P=$R/.venv/bin/python
O=$R/ledgers/M2/scripts/M2-e-r1/g1_grader_staged.out
{
  for s in 0 7 23; do
    D=$(mktemp -d /tmp/m2e_r1b/staged.XXXX)
    cp "$R/course/modules/M/M2/grader/test_project.py" "$R/course/modules/M/M2/grader/instance.py" "$D/"
    cp "$R/course/modules/M/M2/grader/reference.py" "$D/sensitivity_engine.py"
    echo "== seed $s collect-only"
    (cd "$D" && QF_SEED=$s PYTHONHASHSEED=0 $P -I -m pytest --collect-only -q -p no:cacheprovider test_project.py | tail -1)
    echo "== seed $s run, warnings as errors"
    (cd "$D" && QF_SEED=$s PYTHONHASHSEED=0 $P -I -m pytest -q -p no:cacheprovider -W error test_project.py | tail -1)
  done
  echo "exit 0"
} > "$O" 2>&1
tail -3 "$O"
