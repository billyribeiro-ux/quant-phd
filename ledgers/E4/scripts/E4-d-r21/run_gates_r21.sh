#!/bin/bash
# Round-20 verifier gates for E4 slice d, run from the checkout root (pin 6d22ff56).
cd "$(dirname "$0")/../../../.." || exit 1
OUT=ledgers/E4/scripts/E4-d-r21/out
run() { name=$1; shift; { "$@" ; echo "EXIT=$?"; } > "$OUT/$name.txt" 2>&1; }
run check_pages_E4 .venv/bin/python tools/check_pages.py --unit E4
run check_dag_E4 .venv/bin/python tools/check_dag.py --unit E4
run check_projects_E4 .venv/bin/python tools/check_projects.py --unit E4
run run_labs_E4_project .venv/bin/python tools/run_labs.py --unit E4 --page project.html
run run_graders_E4_0_49 .venv/bin/python tools/run_graders.py --unit E4 --seeds 0-49
run mutate_graders_E4_0_9 .venv/bin/python tools/mutate_graders.py --unit E4 --seeds 0-9
run page_smoke_E4_project .venv/bin/python tools/page_smoke.py --unit E4 --pages project.html
run verify_refs_E4_offline .venv/bin/python tools/verify_refs.py --offline --unit E4
run ruff_check .venv/bin/ruff check .
run ruff_format .venv/bin/ruff format --check .
run mypy .venv/bin/mypy --no-incremental
run pytest_labs .venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_page_smoke.py
echo done > "$OUT/gates_done"
