#!/bin/sh
# Command rows for E3 slice a round 4 (hub index.html, L01-L03 and twins), run from the verifier checkout root.
set -u
P=.venv/bin/python
echo "== check_pages"; $P tools/check_pages.py --unit E3; echo "exit $?"
echo "== check_dag"; $P tools/check_dag.py --all | grep E3; echo "exit ${PIPESTATUS:-?}"
echo "== run_labs"; for p in L01 L02 L03; do $P tools/run_labs.py --unit E3 --page $p; echo "exit $? $p"; done
echo "== twins"; for f in 01 02 03; do $P -I -W error tests/labs/E3/lab-E3-L$f-1.py >/dev/null; echo "twin L$f exit $?"; done
echo "== ruff"; .venv/bin/ruff check tests/labs/E3 && .venv/bin/ruff format --check tests/labs/E3; echo "exit $?"
echo "== mypy"; .venv/bin/mypy --no-incremental tests/labs/E3/lab-E3-L01-1.py tests/labs/E3/lab-E3-L02-1.py tests/labs/E3/lab-E3-L03-1.py; echo "exit $?"
echo "== pytest labs"; $P -m pytest tests/test_labs.py -k E3 -q; echo "exit $?"
echo "== verify_refs offline"; $P tools/verify_refs.py --offline; echo "exit $?"
echo "== page_smoke"; $P tools/page_smoke.py --unit E3 2>&1 | tail -20; echo "exit $?"
