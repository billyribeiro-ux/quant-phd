#!/bin/bash
# Round 14 gate runs for SC1-d on the pin 8e5751c (run from the checkout root).
cd /Users/billyribeiro/.fanout/wt/verifyE14-SC1-d || exit 1
O=ledgers/SC1/scripts/SC1-d-r14/out
run() { name="$1"; shift; { echo "\$ $*"; "$@"; echo "EXIT=$?"; } > "$O/$name.txt" 2>&1; }
run check_pages_unit .venv/bin/python tools/check_pages.py --unit SC1
run check_dag_unit .venv/bin/python tools/check_dag.py --unit SC1
run check_projects_unit .venv/bin/python tools/check_projects.py --unit SC1
run run_labs_unit .venv/bin/python tools/run_labs.py --unit SC1
run run_graders_unit .venv/bin/python tools/run_graders.py --unit SC1 --seeds 0-49
run mutate_graders_unit .venv/bin/python tools/mutate_graders.py --unit SC1 --seeds 0-9
run page_smoke_sc1_project .venv/bin/python tools/page_smoke.py --unit SC1 --pages project
run verify_refs_unit_sc1 .venv/bin/python tools/verify_refs.py --unit SC1
run ruff_check .venv/bin/ruff check course/modules/SC/SC1/grader tests/labs/SC1
run ruff_format .venv/bin/ruff format --check course/modules/SC/SC1/grader tests/labs/SC1
run mypy_nocache .venv/bin/mypy --no-incremental
run pytest_labs .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_memo_exemplars.py
run collect_only_grader .venv/bin/pytest --collect-only -q course/modules/SC/SC1/grader/test_project.py
run collect_only_grader_count .venv/bin/python -m pytest --collect-only -q course/modules/SC/SC1/grader/test_project.py
for i in 1 2 3; do run twin_project_$i .venv/bin/python -I -W error tests/labs/SC1/lab-SC1-project-$i.py; done
echo done > "$O/ALL_DONE"
