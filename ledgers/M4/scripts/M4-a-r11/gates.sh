#!/bin/bash
# Round 11 gate run for M4 slice a (verifier). Run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyD11-M4-a || exit 1
PY=.venv/bin/python
echo "== check_pages --unit M4"; $PY tools/check_pages.py --unit M4; echo "EXIT $?"
echo "== check_dag --unit M4"; $PY tools/check_dag.py --unit M4; echo "EXIT $?"
echo "== check_projects --unit M4"; $PY tools/check_projects.py --unit M4; echo "EXIT $?"
echo "== run_labs --unit M4"; $PY tools/run_labs.py --unit M4; echo "EXIT $?"
echo "== page_smoke --unit M4 --pages index L01 L02 L03 L04"; $PY tools/page_smoke.py --unit M4 --pages index L01 L02 L03 L04; echo "EXIT $?"
echo "== ruff check"; .venv/bin/ruff check tests/labs/M4 course/modules/M/M4; echo "EXIT $?"
echo "== ruff format --check"; .venv/bin/ruff format --check tests/labs/M4; echo "EXIT $?"
echo "== mypy --no-incremental"; .venv/bin/mypy --no-incremental; echo "EXIT $?"
echo "== verify_refs --offline"; $PY tools/verify_refs.py --offline; echo "EXIT $?"
echo "== build_site --check"; $PY tools/build_site.py --check; echo "EXIT $?"
echo "== render_curriculum + diff"; $PY tools/render_curriculum.py && git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json; echo "EXIT $?"
echo "== fetch_data --check"; $PY tools/fetch_data.py --check; echo "EXIT $?"
echo "== git status (tracked)"; git status --short | grep -v '^??' ; echo "EXIT $?"
