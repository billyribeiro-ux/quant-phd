#!/bin/bash
# Round 16, FC1-c delta verification gates. Run from the checkout root; each exit code is recorded in out/summary.txt.
cd /Users/billyribeiro/.fanout/wt/verifyD16-FC1-c || exit 1
OUT=ledgers/FC1/scripts/FC1-c-r16/out
mkdir -p "$OUT"
rm -f "$OUT/summary.txt"
run() { name="$1"; shift; "$@" > "$OUT/$name.out" 2>&1; echo "EXIT=$? $name" >> "$OUT/summary.txt"; }
run check_pages_unit .venv/bin/python tools/check_pages.py --unit FC1
run check_dag_unit .venv/bin/python tools/check_dag.py --unit FC1
run check_projects_unit .venv/bin/python tools/check_projects.py --unit FC1
run run_labs_fc1 .venv/bin/python tools/run_labs.py --unit FC1
run page_smoke_project .venv/bin/python tools/page_smoke.py --unit FC1 --pages project
run ruff_check_scope .venv/bin/ruff check course/modules/FC/FC1/grader tests/labs/FC1 ledgers/FC1/scripts/FC1-c-r16
run ruff_format_scope .venv/bin/ruff format --check course/modules/FC/FC1/grader tests/labs/FC1
run mypy_repo .venv/bin/mypy --no-incremental
run pytest_targeted .venv/bin/pytest -q tests/test_curriculum.py tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py -k "FC1 or project or page"
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run mypy_grader_strict .venv/bin/mypy --strict --ignore-missing-imports course/modules/FC/FC1/grader/reference.py course/modules/FC/FC1/grader/starter.py course/modules/FC/FC1/grader/instance.py
