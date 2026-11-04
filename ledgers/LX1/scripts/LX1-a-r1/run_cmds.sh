#!/bin/bash
# LX1-a round 1 command rows, run from the verifier checkout root.
set -u
OUT=ledgers/LX1/scripts/LX1-a-r1/out
mkdir -p "$OUT"
run() { name=$1; shift; "$@" > "$OUT/$name.txt" 2>&1; echo "$name exit=$?"; }
run check_pages .venv/bin/python tools/check_pages.py --unit LX1
run check_dag .venv/bin/python tools/check_dag.py --unit LX1
run check_projects .venv/bin/python tools/check_projects.py --unit LX1
run run_labs_unit .venv/bin/python tools/run_labs.py --unit LX1
run ruff_labs .venv/bin/ruff check tests/labs/LX1
run ruff_format_labs .venv/bin/ruff format --check tests/labs/LX1
run mypy_labs .venv/bin/mypy --no-incremental tests/labs/LX1
run fetch_data_check .venv/bin/python tools/fetch_data.py --check
# Additional rows (run later in round 1): page_smoke --unit LX1 --pages index L01 L02; verify_refs --unit LX1 (live); verify_refs --offline; pytest subset; check_pages etc. See out/.
