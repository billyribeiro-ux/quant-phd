#!/bin/sh
# Verifier gate commands, M3 slice a, round 2 (run from the checkout root; outputs in out/).
# Each command was run once at pin 9294b914; exit codes are appended to the outputs.
O=ledgers/M3/scripts/M3-a-r2/out
.venv/bin/python tools/check_pages.py --unit M3 > $O/check_pages_M3.out 2>&1
.venv/bin/python tools/check_dag.py --unit M3 > $O/check_dag_M3.out 2>&1
.venv/bin/python tools/check_projects.py --unit M3 > $O/check_projects_M3.out 2>&1
.venv/bin/python tools/run_labs.py --unit M3 > $O/run_labs_M3.out 2>&1
.venv/bin/python tools/page_smoke.py --unit M3 --pages index L01 L02 L03 > $O/page_smoke_slice_a.out 2>&1
.venv/bin/ruff check . > $O/ruff_check.out 2>&1
.venv/bin/ruff format --check . > $O/ruff_format.out 2>&1
.venv/bin/mypy --no-incremental > $O/mypy.out 2>&1
.venv/bin/python -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -q > $O/pytest_relevant.out 2>&1
.venv/bin/python tools/verify_refs.py --offline > $O/verify_refs_offline.out 2>&1
.venv/bin/python tools/verify_refs.py --unit M3 > $O/verify_refs_M3_live.out 2>&1
.venv/bin/python tools/build_site.py --check > $O/build_site_check.out 2>&1
.venv/bin/python -I -W error $O/twin_vs_page.py > $O/out/twin_vs_page.out 2>&1
.venv/bin/python -I -W error $O/recheck_numbers.py > $O/out/recheck_numbers.out 2>&1
.venv/bin/python -I -W error $O/cards_scan_verifier_r2.py > $O/out/cards_scan_r2.out 2>&1
.venv/bin/python -I -W error $O/banned_scan_r2.py > $O/out/banned_scan_r2.out 2>&1
