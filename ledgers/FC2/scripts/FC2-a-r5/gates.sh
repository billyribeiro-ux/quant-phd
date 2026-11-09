#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyS5-FC2-a
P=.venv/bin/python
echo "== check_pages"; $P tools/check_pages.py --unit FC2; echo "exit $?"
echo "== check_dag"; $P tools/check_dag.py --unit FC2; echo "exit $?"
echo "== check_projects"; $P tools/check_projects.py --unit FC2; echo "exit $?"
echo "== page_smoke FC2 index+L01-L03"; $P tools/page_smoke.py --help 2>&1 | head -20; echo "exit $?"
echo "== run_labs"; $P tools/run_labs.py --help 2>&1 | head -20
echo "== verify_refs"; $P tools/verify_refs.py --offline; echo "exit $?"
echo "== ruff"; .venv/bin/ruff check tests/labs/FC2/lab-FC2-L01-1.py tests/labs/FC2/lab-FC2-L02-1.py tests/labs/FC2/lab-FC2-L03-1.py; echo "exit $?"
.venv/bin/ruff format --check tests/labs/FC2/; echo "exit $?"
echo "== mypy"; .venv/bin/mypy --no-incremental tests/labs/FC2/lab-FC2-L01-1.py tests/labs/FC2/lab-FC2-L02-1.py tests/labs/FC2/lab-FC2-L03-1.py; echo "exit $?"
