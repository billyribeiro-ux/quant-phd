#!/bin/bash
# Round 1 (closing delta, slice a) gate run at pin 95f3f8cb. Each command's exit code and output are recorded.
cd /Users/billyribeiro/.fanout/wt/verifyF11-FC1-a || exit 1
OUT=ledgers/FC1/scripts/FC1-a-r1/out
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
run pytest_slice .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py tests/test_refs.py tests/test_docs_figures.py
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run build_site_check .venv/bin/python tools/build_site.py --check
run fetch_data_check .venv/bin/python tools/fetch_data.py --check
run page_smoke_fc1 .venv/bin/python tools/page_smoke.py --unit FC1 --pages index L01 L02 L03
for t in L01 L02 L03; do run twin_$t .venv/bin/python -I -W error tests/labs/FC1/lab-FC1-$t-1.py; done
