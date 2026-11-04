#!/bin/sh
# BK4-b round 4 gate run, from the checkout root. Output is captured to gates.out by the caller.
set -u
V=.venv/bin/python
echo "== check_pages L04"; $V tools/check_pages.py --unit BK4 --page L04; echo "exit $?"
echo "== check_pages L05"; $V tools/check_pages.py --unit BK4 --page L05; echo "exit $?"
echo "== check_dag"; $V tools/check_dag.py --unit BK4; echo "exit $?"
echo "== check_projects"; $V tools/check_projects.py --unit BK4; echo "exit $?"
echo "== run_labs L04"; $V tools/run_labs.py --unit BK4 --page L04; echo "exit $?"
echo "== run_labs L05"; $V tools/run_labs.py --unit BK4 --page L05; echo "exit $?"
echo "== twin alone and page equality"; $V -I ledgers/BK4/scripts/BK4-b-r4/twin_and_page.py "$PWD" "$PWD/$V"; echo "exit $?"
echo "== page_smoke L04"; $V tools/page_smoke.py --unit BK4 --pages L04 | tail -2; echo "exit ${PIPESTATUS:-$?}"
echo "== page_smoke L05"; $V tools/page_smoke.py --unit BK4 --pages L05 | tail -2
echo "== ruff twins"; $V -m ruff check tests/labs/BK4/lab-BK4-L04-1.py tests/labs/BK4/lab-BK4-L05-1.py; $V -m ruff format --check tests/labs/BK4/lab-BK4-L04-1.py tests/labs/BK4/lab-BK4-L05-1.py
echo "== mypy twins"; $V -m mypy --no-incremental tests/labs/BK4/lab-BK4-L04-1.py tests/labs/BK4/lab-BK4-L05-1.py
echo "== pytest labs"; $V -m pytest tests/test_labs.py -k "BK4 and (L04 or L05)" -v 2>&1 | tail -1
echo "== verify_refs offline"; $V tools/verify_refs.py --offline | tail -1
echo "== verify_refs unit"; $V tools/verify_refs.py --unit BK4 | tail -1
echo "== recompute"; $V -I ledgers/BK4/scripts/BK4-b-r4/recompute_r4.py | tail -3
