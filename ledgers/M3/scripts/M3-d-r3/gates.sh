#!/bin/bash
# Gate commands for M3-d round 3, run from the verifier checkout (pin a007712). Output goes to out/.
set -u
R=/Users/billyribeiro/.fanout/wt/verifyD3-M3-d
cd "$R" || exit 1
O=ledgers/M3/scripts/M3-d-r3/out
.venv/bin/python tools/check_pages.py --all > $O/check_pages.out 2>&1; echo "exit $?" >> $O/check_pages.out
.venv/bin/python tools/check_dag.py --all > $O/check_dag.out 2>&1; echo "exit $?" >> $O/check_dag.out
.venv/bin/python tools/check_projects.py --all > $O/check_projects.out 2>&1; echo "exit $?" >> $O/check_projects.out
.venv/bin/python tools/run_graders.py --unit M3 --seeds 0-49 > $O/run_graders.out 2>&1; echo "exit $?" >> $O/run_graders.out
.venv/bin/python tools/run_labs.py --unit M3 > $O/run_labs.out 2>&1; echo "exit $?" >> $O/run_labs.out
for p in project L01 L02 L03 L04 L05 L06 L07 L08 L09 index; do .venv/bin/python tools/page_smoke.py --unit M3 --pages $p.html > $O/page_smoke_$p.out 2>&1; echo "exit $?" >> $O/page_smoke_$p.out; done
.venv/bin/ruff check course/modules/M/M3/grader tests/labs/M3 > $O/ruff.out 2>&1; echo "exit $?" >> $O/ruff.out
.venv/bin/ruff format --check course/modules/M/M3/grader tests/labs/M3 >> $O/ruff.out 2>&1; echo "exit $?" >> $O/ruff.out
.venv/bin/mypy --no-incremental course/modules/M/M3/grader/reference.py course/modules/M/M3/grader/instance.py course/modules/M/M3/grader/starter.py > $O/mypy.out 2>&1; echo "exit $?" >> $O/mypy.out
.venv/bin/python tools/verify_refs.py --offline > $O/verify_refs_offline.out 2>&1; echo "exit $?" >> $O/verify_refs_offline.out
.venv/bin/python tools/mutate_graders.py --unit M3 --seeds 0-9 > $O/mutate_M3_seeds0-9.out 2>&1; echo "exit $?" >> $O/mutate_M3_seeds0-9.out
echo GATES_DONE >> $O/done.txt
