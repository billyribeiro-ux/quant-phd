#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyS9-FC2-b
S=ledgers/FC2/scripts/FC2-b-r9
P=.venv/bin/python
echo "== check_pages"; $P tools/check_pages.py --unit FC2; echo "exit $?"
echo "== check_dag"; $P tools/check_dag.py --unit FC2; echo "exit $?"
echo "== check_projects"; $P tools/check_projects.py --unit FC2; echo "exit $?"
echo "== run_labs unit"; $P tools/run_labs.py --unit FC2; echo "exit $?"
for p in L04 L05 L06; do echo "== run_labs $p"; $P tools/run_labs.py --unit FC2 --page $p; echo "exit $?"; done
for p in L04 L05 L06; do echo "== page_smoke $p"; $P tools/page_smoke.py --unit FC2 --pages $p; echo "exit $?"; done
echo "== ruff"; .venv/bin/ruff check tests/labs/FC2; .venv/bin/ruff format --check tests/labs/FC2; echo "exit $?"
echo "== verify_refs"; $P tools/verify_refs.py --offline; echo "exit $?"
echo "== pytest labs FC2"; $P -m pytest tests/test_labs.py -k FC2 -q 2>&1 | tail -3
echo "== pytest page/run_labs"; $P -m pytest tests/test_page_checks.py tests/test_run_labs.py -q 2>&1 | tail -3
echo "== mypy"; .venv/bin/mypy --no-incremental 2>&1 | tail -2
echo "== run_graders"; $P tools/run_graders.py --unit FC2 2>&1 | tail -4; echo "exit $?"
echo "== mutate_graders"; $P tools/mutate_graders.py --unit FC2 2>&1 | tail -15; echo "exit $?"
echo DONE
