#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyS5-FC2-c
S=ledgers/FC2/scripts/FC2-c-r5
run() { name=$1; shift; { echo "\$ $*"; "$@"; echo "exit $?"; } > $S/$name.out 2>&1; }
run check_dag_unit .venv/bin/python tools/check_dag.py --unit FC2
run check_projects_unit .venv/bin/python tools/check_projects.py --unit FC2
run check_pages_all .venv/bin/python tools/check_pages.py --all
run run_labs_L07 .venv/bin/python tools/run_labs.py --unit FC2 --page L07
run run_labs_L08 .venv/bin/python tools/run_labs.py --unit FC2 --page L08
run run_labs_unit .venv/bin/python tools/run_labs.py --unit FC2
run twin_L07_isolated .venv/bin/python -I -W error tests/labs/FC2/lab-FC2-L07-1.py
run twin_L08_isolated .venv/bin/python -I -W error tests/labs/FC2/lab-FC2-L08-1.py
run pytest_labs .venv/bin/python -m pytest tests/test_labs.py -k "FC2 and (L07 or L08)" -rA -q
run pytest_tooling .venv/bin/python -m pytest tests/test_page_checks.py tests/test_run_labs.py -q
run ruff_check .venv/bin/ruff check .
run ruff_format .venv/bin/ruff format --check .
run mypy_full .venv/bin/mypy --no-incremental
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run page_smoke .venv/bin/python tools/page_smoke.py --unit FC2 --pages L07 L08
echo DONE > $S/gates_done.flag
