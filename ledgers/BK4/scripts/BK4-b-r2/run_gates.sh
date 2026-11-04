#!/bin/bash
# Round-2 verifier gate commands for BK4 slice b (L04, L05, twins). Run from the checkout root.
cd "$(dirname "$0")/../../../.." || exit 1
P=.venv/bin/python
echo "== check_pages L04"; $P tools/check_pages.py --unit BK4 --page L04; echo "exit=$?"
echo "== check_pages L05"; $P tools/check_pages.py --unit BK4 --page L05; echo "exit=$?"
echo "== check_dag BK4"; $P tools/check_dag.py --unit BK4; echo "exit=$?"
echo "== check_projects BK4"; $P tools/check_projects.py --unit BK4; echo "exit=$?"
echo "== run_labs L04"; $P tools/run_labs.py --unit BK4 --page L04; echo "exit=$?"
echo "== run_labs L05"; $P tools/run_labs.py --unit BK4 --page L05; echo "exit=$?"
echo "== page_smoke L04 L05"; $P tools/page_smoke.py --unit BK4 --pages L04 L05; echo "exit=$?"
echo "== pytest labs"; $P -m pytest tests/test_labs.py -k 'BK4 and (L04 or L05)' -q; echo "exit=$?"
echo "== ruff twins"; .venv/bin/ruff check tests/labs/BK4/lab-BK4-L04-1.py tests/labs/BK4/lab-BK4-L05-1.py; echo "exit=$?"
echo "== ruff format twins"; .venv/bin/ruff format --check tests/labs/BK4/lab-BK4-L04-1.py tests/labs/BK4/lab-BK4-L05-1.py; echo "exit=$?"
echo "== mypy twins"; .venv/bin/mypy --no-incremental tests/labs/BK4/lab-BK4-L04-1.py tests/labs/BK4/lab-BK4-L05-1.py; echo "exit=$?"
echo "== verify_refs BK4"; $P tools/verify_refs.py --unit BK4; echo "exit=$?"
