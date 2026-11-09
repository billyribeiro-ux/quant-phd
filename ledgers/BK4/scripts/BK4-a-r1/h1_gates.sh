#!/bin/bash
# BK4 slice a closing delta round 1 gates (verifier H1), run from the verifier checkout root
cd /Users/billyribeiro/.fanout/wt/verifyH1-BK4-a || exit 1
O=ledgers/BK4/scripts/BK4-a-r1/out
PY=.venv/bin/python
mkdir -p $O
{ echo "+ check_pages --unit BK4"; $PY tools/check_pages.py --unit BK4; echo "exit=$?"; } > $O/h1_check_pages_BK4.txt 2>&1
{ echo "+ check_dag --unit BK4"; $PY tools/check_dag.py --unit BK4; echo "exit=$?"; } > $O/h1_check_dag_BK4.txt 2>&1
{ echo "+ check_projects --unit BK4"; $PY tools/check_projects.py --unit BK4; echo "exit=$?"; } > $O/h1_check_projects_BK4.txt 2>&1
{ echo "+ run_labs --unit BK4"; $PY tools/run_labs.py --unit BK4; echo "exit=$?"; } > $O/h1_run_labs_BK4.txt 2>&1
{ echo "+ page_smoke --unit BK4 --pages index L01 L02 L03"; $PY tools/page_smoke.py --unit BK4 --pages index L01 L02 L03; echo "exit=$?"; } > $O/h1_page_smoke_BK4.txt 2>&1
{ echo "+ ruff check tests/labs/BK4"; $PY -m ruff check tests/labs/BK4; echo "exit=$?"; echo "+ ruff format --check tests/labs/BK4"; $PY -m ruff format --check tests/labs/BK4; echo "exit=$?"; echo "+ mypy --no-incremental tests/labs/BK4"; $PY -m mypy --no-incremental tests/labs/BK4; echo "exit=$?"; } > $O/h1_ruff_mypy_BK4.txt 2>&1
{ echo "+ pytest tests/test_labs.py -k BK4"; $PY -m pytest tests/test_labs.py -k BK4 -q; echo "exit=$?"; echo "+ pytest tests/test_page_checks.py"; $PY -m pytest tests/test_page_checks.py -q; echo "exit=$?"; } > $O/h1_pytest_BK4.txt 2>&1
{ echo "+ verify_refs --offline"; $PY tools/verify_refs.py --offline; echo "exit=$?"; } > $O/h1_verify_refs_offline.txt 2>&1
echo DONE > $O/h1_GATES_DONE
