#!/bin/bash
# Round-12 slice e gate runs on pin 329c1d7f (run from the checkout root).
cd /Users/billyribeiro/.fanout/wt/verifyD12-E3-e || exit 1
O=ledgers/E3/scripts/E3-e-r12
PY=.venv/bin/python
echo "== check_projects E3"; $PY tools/check_projects.py --unit E3 2>&1; echo "rc=$?"
echo "== check_pages E3"; $PY tools/check_pages.py --unit E3 2>&1; echo "rc=$?"
echo "== check_dag E3"; $PY tools/check_dag.py --unit E3 2>&1; echo "rc=$?"
echo "== run_labs E3 project"; $PY tools/run_labs.py --unit E3 --page project 2>&1; echo "rc=$?"
echo "== run_graders E3 0-49"; $PY tools/run_graders.py --unit E3 --seeds 0-49 2>&1 | tail -40; echo "rc=${PIPESTATUS[0]}"
echo "== verify_refs offline"; $PY tools/verify_refs.py --offline 2>&1 | tail -5; echo "rc=$?"
echo "== ruff"; .venv/bin/ruff check course/modules/E/E3/grader tests/labs/E3 2>&1; .venv/bin/ruff format --check course/modules/E/E3/grader tests/labs/E3 2>&1
echo "== mypy grader"; cd course/modules/E/E3/grader && /Users/billyribeiro/.fanout/wt/verifyD12-E3-e/.venv/bin/mypy --strict --no-incremental reference.py starter.py instance.py test_project.py 2>&1 | tail -5; cd /Users/billyribeiro/.fanout/wt/verifyD12-E3-e
echo "== page_smoke project"; $PY tools/page_smoke.py --unit E3 --pages project 2>&1 | tail -40; echo "rc=${PIPESTATUS[0]}"
echo "DONE"
