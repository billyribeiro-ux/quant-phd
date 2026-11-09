#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyG1-M3-c || exit 1
O=ledgers/M3/scripts/M3-c-r1/out
run() { name=$1; shift; "$@" > $O/$name.log 2>&1; echo "$name rc=$?"; tail -2 $O/$name.log; }
run check_pages_M3 .venv/bin/python tools/check_pages.py --unit M3
run check_pages_L07 .venv/bin/python tools/check_pages.py --unit M3 --page L07
run check_pages_L08 .venv/bin/python tools/check_pages.py --unit M3 --page L08
run check_pages_L09 .venv/bin/python tools/check_pages.py --unit M3 --page L09
run check_dag_M3 .venv/bin/python tools/check_dag.py --unit M3
run build_site_check .venv/bin/python tools/build_site.py --check
run fetch_data_check .venv/bin/python tools/fetch_data.py --check
run run_labs_M3 .venv/bin/python tools/run_labs.py --unit M3
run run_labs_L07 .venv/bin/python tools/run_labs.py --unit M3 --page L07
run run_labs_L08 .venv/bin/python tools/run_labs.py --unit M3 --page L08
run run_labs_L09 .venv/bin/python tools/run_labs.py --unit M3 --page L09
