#!/bin/bash
# FC1-b round 6 gate runs at pin e896b7a4. Each command writes out/<name>.out and out/<name>.rc
cd /Users/billyribeiro/.fanout/wt/verifyS6-FC1-b || exit 1
O=ledgers/FC1/scripts/FC1-b-r6/out
run() { name=$1; shift; "$@" > $O/$name.out 2>&1; echo $? > $O/$name.rc; }
run check_pages_L04 .venv/bin/python tools/check_pages.py --unit FC1 --page L04
run check_pages_L05 .venv/bin/python tools/check_pages.py --unit FC1 --page L05
run check_pages_unit .venv/bin/python tools/check_pages.py --unit FC1
run check_dag_FC1 .venv/bin/python tools/check_dag.py --unit FC1
run check_projects_FC1 .venv/bin/python tools/check_projects.py --unit FC1
run run_labs_L04 .venv/bin/python tools/run_labs.py --unit FC1 --page L04
run run_labs_L05 .venv/bin/python tools/run_labs.py --unit FC1 --page L05
run run_labs_unit .venv/bin/python tools/run_labs.py --unit FC1
run ruff_check .venv/bin/ruff check tests/labs/FC1/lab-FC1-L04-1.py tests/labs/FC1/lab-FC1-L05-1.py
run ruff_format .venv/bin/ruff format --check tests/labs/FC1/lab-FC1-L04-1.py tests/labs/FC1/lab-FC1-L05-1.py
run mypy_twins .venv/bin/mypy --no-incremental tests/labs/FC1/lab-FC1-L04-1.py tests/labs/FC1/lab-FC1-L05-1.py
run pytest_labs .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_curriculum.py
run build_site_check .venv/bin/python tools/build_site.py --check
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run verify_refs_unit_live .venv/bin/python tools/verify_refs.py --unit FC1
run page_smoke_L04_L05 .venv/bin/python tools/page_smoke.py --unit FC1 --pages L04 L05
echo done > $O/_done
