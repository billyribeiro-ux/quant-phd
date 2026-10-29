#!/bin/sh
# Round 8 M5-b mechanical gates, run from checkout at pin ce7b382
cd /Users/billyribeiro/.fanout/wt/verifyB8-M5-b
.venv/bin/python tools/check_pages.py --all 2>&1 | grep -i M5; echo "check_pages rc=${PIPESTATUS:-?}"
.venv/bin/python tools/check_pages.py --all >/tmp/m5b8_cp.txt 2>&1; echo "check_pages_full rc=$?"
.venv/bin/python tools/check_dag.py --all 2>&1 | grep M5
.venv/bin/python tools/check_projects.py --all 2>&1 | grep M5
.venv/bin/python tools/run_labs.py --unit M5 2>&1 | tail -20; echo "run_labs rc=$?"
.venv/bin/python tools/page_smoke.py --unit M5 --pages course/modules/M/M5/L05.html course/modules/M/M5/L06.html course/modules/M/M5/L07.html 2>&1 | tail -10; echo "page_smoke rc=$?"
for t in lab-M5-L05-1 lab-M5-L06-1 lab-M5-L07-1; do .venv/bin/python -I -W error tests/labs/M5/$t.py >/tmp/m5b8_$t.out 2>/tmp/m5b8_$t.err; echo "$t rc=$? stderr_bytes=$(wc -c </tmp/m5b8_$t.err)"; done
.venv/bin/python -m ruff check tests/labs/M5 ; .venv/bin/python -m ruff format --check tests/labs/M5
.venv/bin/mypy --no-incremental 2>&1 | tail -2
