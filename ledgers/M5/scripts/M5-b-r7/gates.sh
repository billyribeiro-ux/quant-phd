#!/bin/sh
# Round 7 M5-b mechanical gates, run from the checkout at pin 7aa909e
cd /Users/billyribeiro/.fanout/wt/verifyB7-M5-b
.venv/bin/python tools/check_pages.py --all | grep M5
.venv/bin/python tools/check_dag.py --all | grep M5
.venv/bin/python tools/check_projects.py --all | grep M5
.venv/bin/python tools/run_labs.py --unit M5
.venv/bin/python tools/page_smoke.py --unit M5 --pages course/modules/M/M5/L05.html course/modules/M/M5/L06.html course/modules/M/M5/L07.html
for t in lab-M5-L05-1 lab-M5-L06-1 lab-M5-L07-1; do .venv/bin/python -I -W error tests/labs/M5/$t.py >/dev/null; echo "$t rc=$?"; done
.venv/bin/python -m ruff check tests/labs/M5
.venv/bin/mypy --no-incremental
