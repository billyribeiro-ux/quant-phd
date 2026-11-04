#!/bin/bash
# Round-5 command gates for CS2 slice d, run from the checkout root (pin 440ed3c).
cd "$(dirname "$0")/../../../.." || exit 1
OUT=ledgers/CS2/scripts/CS2-d-r5
run() { name="$1"; shift; "$@" > "$OUT/$name.txt" 2>&1; echo "$name exit=$?" >> "$OUT/_exit_codes.txt"; }
rm -f "$OUT/_exit_codes.txt"
run g_check_pages .venv/bin/python tools/check_pages.py --unit CS2
run g_check_dag .venv/bin/python tools/check_dag.py --unit CS2
run g_check_projects .venv/bin/python tools/check_projects.py --unit CS2
run g_run_labs .venv/bin/python tools/run_labs.py --unit CS2
run g_run_graders .venv/bin/python tools/run_graders.py --unit CS2 --seeds 0-49
run g_mutate .venv/bin/python tools/mutate_graders.py --unit CS2 --seeds 0-9
run g_page_smoke .venv/bin/python tools/page_smoke.py --unit CS2 --pages project.html --skip-sweep
run g_ruff_check .venv/bin/ruff check .
run g_ruff_format .venv/bin/ruff format --check .
run g_mypy .venv/bin/mypy --no-incremental
run g_verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run g_verify_refs_live .venv/bin/python tools/verify_refs.py --unit CS2
run g_pytest_relevant .venv/bin/pytest -q tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py tests/test_refs.py
echo done >> "$OUT/_exit_codes.txt"
