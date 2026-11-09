#!/bin/bash
# Round-6 gate record for M2 slice b (pin e896b7a4). Run from the verifier checkout.
cd /Users/billyribeiro/.fanout/wt/verifyS6-M2-b || exit 1
S=ledgers/M2/scripts/M2-b-r6
PY=.venv/bin/python
run() { local name=$1; shift; "$@" > $S/$name.out 2>&1; echo "exit=$?" >> $S/$name.out; echo "$name: $(tail -1 $S/$name.out)"; }
run g01_check_pages_M2      $PY tools/check_pages.py --unit M2
run g02_check_dag_M2        $PY tools/check_dag.py --unit M2
run g03_check_projects_M2   $PY tools/check_projects.py --unit M2
run g04_run_labs_M2         $PY tools/run_labs.py --unit M2
run g04b_check_pages_all    $PY tools/check_pages.py --all
run g04c_check_dag_all      $PY tools/check_dag.py --all
run g04d_check_projects_all $PY tools/check_projects.py --all
run g06_page_smoke_L07_L12  $PY tools/page_smoke.py --unit M2 --pages L07 L08 L09 L10 L11 L12
run g07_ruff_check_M2_twins .venv/bin/ruff check tests/labs/M2
run g07b_ruff_format_M2_twins .venv/bin/ruff format --check tests/labs/M2
run g08_mypy_all            $PY -m mypy --no-incremental
run g09_pytest_labs_pagechecks $PY -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_refs.py tests/test_page_smoke.py -k 'M2 or lab or page or refs' -q
run g10_verify_refs_offline $PY tools/verify_refs.py --offline
run g11_build_site_check    $PY tools/build_site.py --check
run g12_verify_refs_live_M2 $PY tools/verify_refs.py --unit M2
