#!/bin/bash
# Round-3 slice b gates (fast, offline). Run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyS3-M3-b
echo "== check_pages --unit M3"; .venv/bin/python tools/check_pages.py --unit M3; echo "exit=$?"
echo "== check_dag --unit M3"; .venv/bin/python tools/check_dag.py --unit M3; echo "exit=$?"
echo "== check_projects --unit M3"; .venv/bin/python tools/check_projects.py --unit M3; echo "exit=$?"
echo "== run_labs --unit M3 --page L04"; .venv/bin/python tools/run_labs.py --unit M3 --page L04; echo "exit=$?"
echo "== run_labs --unit M3 --page L05"; .venv/bin/python tools/run_labs.py --unit M3 --page L05; echo "exit=$?"
echo "== run_labs --unit M3 --page L06"; .venv/bin/python tools/run_labs.py --unit M3 --page L06; echo "exit=$?"
echo "== verify_refs --offline --unit M3"; .venv/bin/python tools/verify_refs.py --offline --unit M3; echo "exit=$?"
echo "== ruff check tests/labs/M3"; .venv/bin/ruff check tests/labs/M3; echo "exit=$?"
echo "== ruff format --check tests/labs/M3"; .venv/bin/ruff format --check tests/labs/M3; echo "exit=$?"
echo "== mypy --no-incremental"; .venv/bin/mypy --no-incremental; echo "exit=$?"
