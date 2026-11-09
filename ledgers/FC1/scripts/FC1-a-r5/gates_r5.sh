#!/bin/bash
# Round 5 gate run for FC1-a at pin dde0486b. Each command's exit code and output are recorded.
cd /Users/billyribeiro/.fanout/wt/verifyS5-FC1-a || exit 1
OUT=ledgers/FC1/scripts/FC1-a-r5/out
mkdir -p "$OUT"
rm -f "$OUT/summary.txt"
run() { name="$1"; shift; "$@" > "$OUT/$name.out" 2>&1; echo "EXIT=$? $name" >> "$OUT/summary.txt"; }
run check_pages_unit .venv/bin/python tools/check_pages.py --unit FC1
run check_pages_all .venv/bin/python tools/check_pages.py --all
run check_dag_unit .venv/bin/python tools/check_dag.py --unit FC1
run check_dag_all .venv/bin/python tools/check_dag.py --all
run check_projects_unit .venv/bin/python tools/check_projects.py --unit FC1
run check_projects_all .venv/bin/python tools/check_projects.py --all
run run_labs_fc1 .venv/bin/python tools/run_labs.py --unit FC1
run ruff_check .venv/bin/ruff check .
run ruff_format .venv/bin/ruff format --check .
run mypy_nocache .venv/bin/mypy --no-incremental
run pytest_relevant .venv/bin/pytest -q tests/test_labs.py -k FC1 tests/test_page_checks.py tests/test_page_smoke.py tests/test_refs.py tests/test_run_labs.py tests/test_docs_figures.py
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run build_site_check .venv/bin/python tools/build_site.py --check
run fetch_data_check .venv/bin/python tools/fetch_data.py --check
run page_smoke_fc1 .venv/bin/python tools/page_smoke.py --unit FC1 --pages index L01 L02 L03
