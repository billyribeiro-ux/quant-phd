#!/bin/bash
# Round-9 verifier gate run for SC1 slice d (pin c93dd52). Each command's exit code is recorded.
cd /Users/billyribeiro/.fanout/wt/verifyE9-SC1-d || exit 1
OUT=ledgers/SC1/scripts/SC1-d-r9/out
PY=.venv/bin/python
run() { name=$1; shift; "$@" > "$OUT/$name.txt" 2>&1; echo "$name exit=$?" >> "$OUT/_exits.txt"; }
run check_pages_all $PY tools/check_pages.py --all
run check_dag_all $PY tools/check_dag.py --all
run check_projects_all $PY tools/check_projects.py --all
run run_labs_SC1 $PY tools/run_labs.py --unit SC1
run run_graders_SC1 $PY tools/run_graders.py --unit SC1 --seeds 0-49
run page_smoke_SC1_project $PY tools/page_smoke.py --unit SC1 --pages project
run ruff_check .venv/bin/ruff check .
run ruff_format .venv/bin/ruff format --check .
run mypy .venv/bin/mypy --no-incremental
run pytest_sc1_related $PY -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_memo_exemplars.py -k "SC1 or sc1 or exemplar or memo or labs or run_labs or page"
run verify_refs_offline $PY tools/verify_refs.py --offline
echo DONE >> "$OUT/_exits.txt"
