#!/bin/bash
# Round 7 gate re-run for M2 slice a at HEAD (delta verification).
cd /Users/billyribeiro/.fanout/wt/verifyS7-M2-a || exit 1
O=ledgers/M2/scripts/M2-a-r7
run() { name=$1; shift; "$@" > "$O/$name.out" 2>&1; echo "EXIT $?" >> "$O/$name.out"; }
run g01_check_pages .venv/bin/python tools/check_pages.py --unit M2
run g02_check_dag .venv/bin/python tools/check_dag.py --unit M2
run g03_run_labs .venv/bin/python tools/run_labs.py --unit M2
for n in 1 2 3 4 5 6; do run g04_twin_L0$n .venv/bin/python -I -W error tests/labs/M2/lab-M2-L0$n-1.py; done
run g05_pytest_labs .venv/bin/pytest tests/test_labs.py -k 'M2 and (L01 or L02 or L03 or L04 or L05 or L06)' -q
run g06_page_smoke .venv/bin/python tools/page_smoke.py --unit M2 --pages index L01 L02 L03 L04 L05 L06 --skip-sweep
run g07_ruff_check .venv/bin/ruff check tests/labs/M2
run g07_ruff_format .venv/bin/ruff format --check tests/labs/M2
run g07_mypy .venv/bin/mypy --no-incremental tests/labs/M2/lab-M2-L01-1.py tests/labs/M2/lab-M2-L02-1.py tests/labs/M2/lab-M2-L03-1.py tests/labs/M2/lab-M2-L04-1.py tests/labs/M2/lab-M2-L05-1.py tests/labs/M2/lab-M2-L06-1.py
run g08_verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run g08_verify_refs_unit_M2 .venv/bin/python tools/verify_refs.py --unit M2
run g09_check_projects .venv/bin/python tools/check_projects.py --unit M2
run g10_build_site_check .venv/bin/python tools/build_site.py --check
run g10_pytest_build_site .venv/bin/pytest tests/test_build_site.py -q
echo ALLDONE > "$O/done.flag"
