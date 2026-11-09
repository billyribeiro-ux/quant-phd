#!/bin/bash
# FC2 slice b round 3: gate commands run from the checkout root; outputs next to this script.
set -u
ROOT=/Users/billyribeiro/.fanout/wt/verifyS3-FC2-b
OUT=$ROOT/ledgers/FC2/scripts/FC2-b-r3
cd "$ROOT" || exit 1
run() { name=$1; shift; "$@" > "$OUT/$name.txt" 2>&1; echo "$name exit=$?" >> "$OUT/gate_exit_codes.txt"; }
run check_pages .venv/bin/python tools/check_pages.py --unit FC2
run check_dag .venv/bin/python tools/check_dag.py --unit FC2
run check_projects .venv/bin/python tools/check_projects.py --unit FC2
run run_labs_unit .venv/bin/python tools/run_labs.py --unit FC2
run run_labs_L04 .venv/bin/python tools/run_labs.py --unit FC2 --page L04
run run_labs_L05 .venv/bin/python tools/run_labs.py --unit FC2 --page L05
run run_labs_L06 .venv/bin/python tools/run_labs.py --unit FC2 --page L06
run run_graders .venv/bin/python tools/run_graders.py --unit FC2 --seeds 0-49
run ruff_check .venv/bin/ruff check tests/labs/FC2/lab-FC2-L04-1.py tests/labs/FC2/lab-FC2-L05-1.py tests/labs/FC2/lab-FC2-L06-1.py
run ruff_format .venv/bin/ruff format --check tests/labs/FC2/lab-FC2-L04-1.py tests/labs/FC2/lab-FC2-L05-1.py tests/labs/FC2/lab-FC2-L06-1.py
run mypy .venv/bin/mypy --no-incremental
run pytest_labs_fc2 .venv/bin/pytest tests/test_labs.py -k FC2 -q
run pytest_checks .venv/bin/pytest tests/test_page_checks.py tests/test_run_labs.py -q
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run page_smoke_L04_L05_L06 .venv/bin/python tools/page_smoke.py --unit FC2 --pages L04 L05 L06
echo done >> "$OUT/gate_exit_codes.txt"
