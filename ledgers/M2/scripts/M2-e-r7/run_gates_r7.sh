#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyD7-M2-e
S=ledgers/M2/scripts/M2-e-r7
PY=.venv/bin/python
run(){ name=$1; shift; "$@" > $S/$name.out 2>&1; echo "rc=$?" >> $S/$name.out; }
run git_head git rev-parse HEAD
run check_pages $PY tools/check_pages.py --unit M2
run check_dag $PY tools/check_dag.py --unit M2
run check_projects $PY tools/check_projects.py --unit M2
run run_graders $PY tools/run_graders.py --unit M2 --seeds 0-49
run run_labs_M2 $PY tools/run_labs.py --unit M2
run page_smoke_M2 $PY tools/page_smoke.py --unit M2
run ruff_check $PY -m ruff check course/modules/M/M2/grader tests/labs/M2
run ruff_format $PY -m ruff format --check course/modules/M/M2/grader tests/labs/M2
run mypy_labs $PY -m mypy --no-incremental tests/labs/M2
run verify_refs_offline $PY tools/verify_refs.py --offline
run pytest_labs_M2 $PY -m pytest -q tests/test_labs.py tests/test_run_labs.py -k M2
run pytest_collect $PY -m pytest --collect-only -q course/modules/M/M2/grader/test_project.py
run pytest_seed0 env QF_SEED=0 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error course/modules/M/M2/grader/test_project.py
run pytest_seed7 env QF_SEED=7 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error course/modules/M/M2/grader/test_project.py
run pytest_seed49 env QF_SEED=49 $PY -m pytest -q -p no:cacheprovider --assert=plain -W error course/modules/M/M2/grader/test_project.py
run mutate_M2_r7 $PY tools/mutate_graders.py --unit M2 --seeds 0-9
echo DONE > $S/gates_done.flag
