#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyC8-E5-b
P=.venv/bin/python
echo "== check_pages"; $P tools/check_pages.py --unit E5 2>&1 | tail -5; echo "rc=$?"
echo "== check_dag"; $P tools/check_dag.py --unit E5 2>&1 | tail -5
echo "== check_projects"; $P tools/check_projects.py --all 2>&1 | tail -5
echo "== run_labs"; $P tools/run_labs.py --unit E5 2>&1 | tail -15
echo "== build_site"; $P tools/build_site.py --check 2>&1 | tail -3
echo "== verify_refs"; $P tools/verify_refs.py --offline 2>&1 | tail -3
