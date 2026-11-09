#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyG1-FC2-b
P=.venv/bin/python
echo "== HEAD"; git rev-parse HEAD
echo "== check_pages FC2"; $P tools/check_pages.py --unit FC2; echo "exit $?"
echo "== check_dag FC2"; $P tools/check_dag.py --unit FC2; echo "exit $?"
echo "== check_projects FC2"; $P tools/check_projects.py --unit FC2; echo "exit $?"
echo "== page_smoke L04 alone"; $P tools/page_smoke.py --unit FC2 --pages L04; echo "exit $?"
echo "== page_smoke L05 alone"; $P tools/page_smoke.py --unit FC2 --pages L05; echo "exit $?"
echo "== page_smoke L06 alone"; $P tools/page_smoke.py --unit FC2 --pages L06; echo "exit $?"
echo "== run_labs unit FC2"; $P tools/run_labs.py --unit FC2; echo "exit $?"
echo "== mutate_graders FC2 (standing set, ruling 37)"; $P tools/mutate_graders.py --unit FC2 2>&1 | tail -15; echo "exit ${PIPESTATUS[0]}"
echo DONE
