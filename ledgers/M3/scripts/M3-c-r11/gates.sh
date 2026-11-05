#!/bin/bash
# Round-11 gate runs for M3 slice c (L07-L09 and lab twins). Run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyD11-M3-c || exit 1
PY=.venv/bin/python
echo "== check_pages --unit M3"; $PY tools/check_pages.py --unit M3; echo "rc=$?"
for p in L07 L08 L09; do echo "== check_pages --unit M3 --page $p"; $PY tools/check_pages.py --unit M3 --page $p; echo "rc=$?"; done
echo "== check_dag --unit M3"; $PY tools/check_dag.py --unit M3; echo "rc=$?"
echo "== check_projects --unit M3"; $PY tools/check_projects.py --unit M3; echo "rc=$?"
echo "== run_labs --unit M3"; $PY tools/run_labs.py --unit M3; echo "rc=$?"
for p in L07 L08 L09; do echo "== run_labs --unit M3 --page $p"; $PY tools/run_labs.py --unit M3 --page $p; echo "rc=$?"; done
echo "== verify_refs --offline"; $PY tools/verify_refs.py --offline; echo "rc=$?"
echo "== ruff check"; .venv/bin/ruff check tests/labs/M3 course/modules/M/M3/grader; echo "rc=$?"
echo "== ruff format --check"; .venv/bin/ruff format --check tests/labs/M3; echo "rc=$?"
echo "== mypy"; .venv/bin/mypy --no-incremental; echo "rc=$?"
echo "== build_site --check"; $PY tools/build_site.py --check; echo "rc=$?"
echo "== render_curriculum + diff"; $PY tools/render_curriculum.py; echo "rc=$?"; git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json; echo "diffrc=$?"
echo "== fetch_data --check"; $PY tools/fetch_data.py --check; echo "rc=$?"
