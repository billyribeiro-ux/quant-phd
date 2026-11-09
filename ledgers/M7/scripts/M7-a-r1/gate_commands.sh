#!/bin/sh
# Verifier M7 slice a, closing delta round 1. Run from the checkout root at pin 95f3f8cb.
# Each command is run alone; exit code is recorded after the command output.
OUT=ledgers/M7/scripts/M7-a-r1/out
mkdir -p "$OUT"
run() { name="$1"; shift; "$@" > "$OUT/$name.out" 2>&1; echo "$? $name" >> "$OUT/exit_codes.txt"; }
rm -f "$OUT/exit_codes.txt"
run check_pages_unit .venv/bin/python tools/check_pages.py --unit M7
run check_pages_L01 .venv/bin/python tools/check_pages.py --unit M7 --page L01
run check_pages_L02 .venv/bin/python tools/check_pages.py --unit M7 --page L02
run check_pages_L03 .venv/bin/python tools/check_pages.py --unit M7 --page L03
run check_dag_unit .venv/bin/python tools/check_dag.py --unit M7
run check_projects_unit .venv/bin/python tools/check_projects.py --unit M7
run run_labs_L01 .venv/bin/python tools/run_labs.py --unit M7 --page L01
run run_labs_L02 .venv/bin/python tools/run_labs.py --unit M7 --page L02
run run_labs_L03 .venv/bin/python tools/run_labs.py --unit M7 --page L03
run twin_L01 .venv/bin/python -I -W error tests/labs/M7/lab-M7-L01-1.py
run twin_L02 .venv/bin/python -I -W error tests/labs/M7/lab-M7-L02-1.py
run twin_L03 .venv/bin/python -I -W error tests/labs/M7/lab-M7-L03-1.py
run page_smoke_M7 .venv/bin/python tools/page_smoke.py --unit M7 --pages index L01 L02 L03
run ruff_check_twins .venv/bin/ruff check tests/labs/M7/lab-M7-L01-1.py tests/labs/M7/lab-M7-L02-1.py tests/labs/M7/lab-M7-L03-1.py
run ruff_format_twins .venv/bin/ruff format --check tests/labs/M7/lab-M7-L01-1.py tests/labs/M7/lab-M7-L02-1.py tests/labs/M7/lab-M7-L03-1.py
run ruff_check_repo .venv/bin/ruff check .
run ruff_format_repo .venv/bin/ruff format --check .
run mypy_twins_strict .venv/bin/mypy --no-incremental --strict tests/labs/M7/lab-M7-L01-1.py tests/labs/M7/lab-M7-L02-1.py tests/labs/M7/lab-M7-L03-1.py
run mypy_repo .venv/bin/mypy --no-incremental
run pytest_labs_M7 .venv/bin/pytest tests/test_labs.py -k M7 -q
run pytest_collect_M7 .venv/bin/pytest tests/test_labs.py -k M7 --collect-only -q
run verify_refs_offline .venv/bin/python tools/verify_refs.py --offline
run verify_refs_live_M7 .venv/bin/python tools/verify_refs.py --unit M7
run fetch_data_check .venv/bin/python tools/fetch_data.py --check
cat "$OUT/exit_codes.txt"
# Delta-specific checks (outputs in ledgers/M7/scripts/M7-a-r1/): run after the gate commands above.
.venv/bin/python -I ledgers/M7/scripts/M7-a-r1/delta_lab_check.py > ledgers/M7/scripts/M7-a-r1/delta_lab_check.out 2>&1
.venv/bin/python -I ledgers/M7/scripts/M7-a-r1/delta_cards_check.py M7-c004 M7-c018 M7-c041 M7-c050 M7-c229 M7-c226 M7-c227 M7-c228 > ledgers/M7/scripts/M7-a-r1/delta_cards_check.out 2>&1
.venv/bin/python -I ledgers/M7/scripts/M7-a-r1/card_bytes_delta.py 9294b914 HEAD > ledgers/M7/scripts/M7-a-r1/card_bytes_delta.out
.venv/bin/python -I ledgers/M7/scripts/M7-a-r1/scan_text.py > ledgers/M7/scripts/M7-a-r1/scan_text.out 2>&1
