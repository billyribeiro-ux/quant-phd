#!/bin/bash
# Round 7 verifier gate runs for CS2 slice c (L09-L11), run from the checkout root.
cd /Users/billyribeiro/.fanout/wt/verifyB7-CS2-c || exit 1
PY=.venv/bin/python
echo "== check_pages L09 L10 L11"
for p in L09 L10 L11; do $PY tools/check_pages.py --unit CS2 --page $p; echo "exit=$?"; done
echo "== check_dag CS2"; $PY tools/check_dag.py --unit CS2; echo "exit=$?"
echo "== run_labs L09 L10 L11"
for p in L09 L10 L11; do $PY tools/run_labs.py --unit CS2 --page $p; echo "exit=$?"; done
echo "== twins alone under python -I -W error"
for f in L09 L10 L11; do $PY -I -W error tests/labs/CS2/lab-CS2-$f-1.py > /tmp/cs2c_r7_$f.out 2>&1; echo "$f exit=$?"; done
echo "== page_smoke L09 L10 L11 (alone)"; $PY tools/page_smoke.py --unit CS2 --pages L09 L10 L11; echo "exit=$?"
echo "== ruff"; $PY -m ruff check tests/labs/CS2/lab-CS2-L09-1.py tests/labs/CS2/lab-CS2-L10-1.py tests/labs/CS2/lab-CS2-L11-1.py; echo "exit=$?"
$PY -m ruff format --check tests/labs/CS2/lab-CS2-L09-1.py tests/labs/CS2/lab-CS2-L10-1.py tests/labs/CS2/lab-CS2-L11-1.py; echo "exit=$?"
echo "== mypy"; $PY -m mypy --no-incremental tests/labs/CS2/lab-CS2-L09-1.py tests/labs/CS2/lab-CS2-L10-1.py tests/labs/CS2/lab-CS2-L11-1.py; echo "exit=$?"
echo "== pytest test_labs CS2"; $PY -m pytest -q tests/test_labs.py -k CS2 2>&1 | tail -5
echo "== verify_refs offline"; $PY tools/verify_refs.py --offline 2>&1 | tail -3; echo "exit=${PIPESTATUS[0]}"
echo "== check_projects CS2 (informational)"; $PY tools/check_projects.py --unit CS2 2>&1 | tail -3
