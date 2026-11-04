#!/bin/sh
# LX1-c round 2: the gate commands this verifier ran on the pin (run from the repo root). Output in gates_r2.out.
R=.venv/bin
echo "== check_projects --unit LX1"; $R/python tools/check_projects.py --unit LX1; echo "exit=$?"
echo "== check_pages --unit LX1 (lessons, hub, cards; project pages are checked by check_projects)"; $R/python tools/check_pages.py --unit LX1; echo "exit=$?"
echo "== check_dag --unit LX1"; $R/python tools/check_dag.py --unit LX1; echo "exit=$?"
echo "== run_labs --unit LX1"; $R/python tools/run_labs.py --unit LX1; echo "exit=$?"
echo "== page_smoke --unit LX1 --pages project"; $R/python tools/page_smoke.py --unit LX1 --pages project; echo "exit=$?"
echo "== fetch_data --check"; $R/python tools/fetch_data.py --check; echo "exit=$?"
echo "== verify_refs --offline"; $R/python tools/verify_refs.py --offline; echo "exit=$?"
echo "== verify_refs --unit LX1 (live, plain Crossref/issuer requests)"; $R/python tools/verify_refs.py --unit LX1; echo "exit=$?"
echo "== ruff check and format (lab twins)"; $R/ruff check tests/labs/LX1; echo "exit=$?"; $R/ruff format --check tests/labs/LX1; echo "exit=$?"
echo "== mypy --no-incremental (lab twins)"; $R/mypy --no-incremental tests/labs/LX1; echo "exit=$?"
echo "== pytest tests/test_labs.py -k LX1"; $R/python -m pytest -q tests/test_labs.py -k LX1 2>&1 | tail -2; echo "exit=${PIPESTATUS:-na}"
echo "== pytest tests/test_page_checks.py (full file; no test name carries LX1, -k selects 0)"; $R/python -m pytest -q tests/test_page_checks.py 2>&1 | tail -2
echo "== pytest tests/test_run_labs.py"; $R/python -m pytest -q tests/test_run_labs.py 2>&1 | tail -2
