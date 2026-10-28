#!/bin/sh
# CF1 slice c, round 13: command rows, run on the pin eaf6d87 from the checkout root.
set -u
P=.venv/bin/python
echo "== pin"; git rev-parse HEAD
echo "== check_pages"; $P tools/check_pages.py --all; echo "exit $?"
echo "== check_dag"; $P tools/check_dag.py --all; echo "exit $?"
echo "== run_labs"; $P tools/run_labs.py --unit CF1; echo "exit $?"
echo "== page_smoke"; $P tools/page_smoke.py --unit CF1 --pages L05 L06; echo "exit $?"
echo "== verify_refs offline"; $P tools/verify_refs.py --offline; echo "exit $?"
echo "== verify_refs live CF1"; $P tools/verify_refs.py --unit CF1; echo "exit $?"
echo "== ruff twins"; .venv/bin/ruff check tests/labs/CF1/lab-CF1-L05-1.py tests/labs/CF1/lab-CF1-L06-1.py && .venv/bin/ruff format --check tests/labs/CF1/lab-CF1-L05-1.py tests/labs/CF1/lab-CF1-L06-1.py; echo "exit $?"
echo "== mypy twins"; .venv/bin/mypy --no-incremental tests/labs/CF1/lab-CF1-L05-1.py tests/labs/CF1/lab-CF1-L06-1.py; echo "exit $?"
echo "== pytest labs"; $P -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_docs_figures.py 2>&1 | tail -3; echo "exit $?"
echo "== twins alone under -I -W error"
for f in lab-CF1-L05-1 lab-CF1-L06-1; do $P -I -W error tests/labs/CF1/$f.py >/dev/null; echo "$f exit $?"; done
echo "== twin vs page"; $P -I ledgers/CF1/scripts/CF1-c-r13/twin_vs_page.py "$(pwd)"; echo "exit $?"
echo "== L06 output"; $P -I -W error tests/labs/CF1/lab-CF1-L06-1.py > /tmp/cf1-v/c13/l06.out; echo "exit $?"; cat /tmp/cf1-v/c13/l06.out
