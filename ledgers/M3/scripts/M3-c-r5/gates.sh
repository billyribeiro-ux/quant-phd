#!/bin/bash
# Round-5 gate runs for M3 slice c (L07-L09 and twins). Run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyD5-M3-c || exit 1
D=ledgers/M3/scripts/M3-c-r5
P=.venv/bin/python
run() { local name="$1"; shift; "$@" > "$D/$name.log" 2>&1; echo "EXIT=$?" >> "$D/$name.log"; }
run check_pages_M3 $P tools/check_pages.py --unit M3
run check_pages_L07 $P tools/check_pages.py --unit M3 --page L07
run check_pages_L08 $P tools/check_pages.py --unit M3 --page L08
run check_pages_L09 $P tools/check_pages.py --unit M3 --page L09
run check_dag_M3 $P tools/check_dag.py --unit M3
run run_labs_M3 $P tools/run_labs.py --unit M3
run run_labs_L07 $P tools/run_labs.py --unit M3 --page L07
run run_labs_L08 $P tools/run_labs.py --unit M3 --page L08
run run_labs_L09 $P tools/run_labs.py --unit M3 --page L09
run ruff_check .venv/bin/ruff check tests/labs/M3
run ruff_format .venv/bin/ruff format --check tests/labs/M3
run mypy $P -m mypy --no-incremental
run verify_refs_offline $P tools/verify_refs.py --offline
run pytest_slice $P -m pytest tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py -k 'M3 or run_labs or page' -q
run page_smoke_L07 $P tools/page_smoke.py --unit M3 --page L07
run page_smoke_L08 $P tools/page_smoke.py --unit M3 --page L08
run page_smoke_L09 $P tools/page_smoke.py --unit M3 --page L09
echo DONE > $D/DONE
