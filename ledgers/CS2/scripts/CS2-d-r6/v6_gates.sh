#!/bin/bash
# Round-6 verifier command gates for CS2 slice d (checkout pinned at 142ecfc2). Run from the checkout root.
cd "$(dirname "$0")/../../../.." || exit 1
OUT=ledgers/CS2/scripts/CS2-d-r6
run() { name="$1"; shift; "$@" > "$OUT/v6_$name.txt" 2>&1; echo "$name exit=$?" >> "$OUT/v6_exit_codes.txt"; }
rm -f "$OUT/v6_exit_codes.txt"
run check_pages .venv/bin/python tools/check_pages.py --unit CS2
run check_dag .venv/bin/python tools/check_dag.py --unit CS2
run check_projects .venv/bin/python tools/check_projects.py --unit CS2
run run_labs .venv/bin/python tools/run_labs.py --unit CS2
run run_graders .venv/bin/python tools/run_graders.py --unit CS2 --seeds 0-49
run ruff_check .venv/bin/ruff check tests/labs/CS2 course/modules/CS/CS2 ledgers/CS2/mutants ledgers/CS2/scripts/CS2-d-r6
run ruff_format .venv/bin/ruff format --check tests/labs/CS2 course/modules/CS/CS2 ledgers/CS2/mutants
run mypy .venv/bin/mypy --no-incremental
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run pytest_relevant .venv/bin/pytest -q tests/test_memo_exemplars.py tests/test_page_checks.py tests/test_labs.py tests/test_run_labs.py tests/test_refs.py
echo done >> "$OUT/v6_exit_codes.txt"
