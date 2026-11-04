#!/bin/bash
# Round-4 verifier gates for PC3 slice a. Run from the checkout root.
# Each command's output and exit status are appended to outputs/gates.out.
cd /Users/billyribeiro/.fanout/wt/verifyE4-PC3-a || exit 1
OUT=ledgers/PC3/scripts/PC3-a-r4/outputs/gates.out
: > "$OUT"
run() {
  echo "=== \$ $*" >> "$OUT"
  "$@" >> "$OUT" 2>&1
  echo "=== exit=$?" >> "$OUT"
}
PY=.venv/bin/python
run $PY tools/check_pages.py --unit PC3 --page L01
run $PY tools/check_pages.py --unit PC3 --page L02
run $PY tools/check_pages.py --unit PC3 --page L03
run $PY tools/check_pages.py --unit PC3
run $PY tools/check_dag.py --unit PC3
run $PY tools/check_projects.py --unit PC3
run $PY tools/run_labs.py --unit PC3 --page L01
run $PY tools/run_labs.py --unit PC3 --page L02
run $PY tools/run_labs.py --unit PC3 --page L03
run $PY tools/verify_refs.py --offline
run .venv/bin/ruff check tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py
run .venv/bin/ruff format --check tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py
run .venv/bin/mypy --no-incremental tests/labs/PC3/lab-PC3-L01-1.py tests/labs/PC3/lab-PC3-L02-1.py tests/labs/PC3/lab-PC3-L03-1.py
run $PY -m pytest tests/test_labs.py -q -k PC3
run $PY -m pytest tests/test_labs.py --collect-only -q -k PC3
for t in L01 L02 L03; do
  echo "=== twin $t: python -I -W error" >> "$OUT"
  $PY -I -W error tests/labs/PC3/lab-PC3-$t-1.py > ledgers/PC3/scripts/PC3-a-r4/outputs/twin-$t.stdout 2> ledgers/PC3/scripts/PC3-a-r4/outputs/twin-$t.stderr
  echo "=== exit=$?  stdout_lines=$(wc -l < ledgers/PC3/scripts/PC3-a-r4/outputs/twin-$t.stdout) stderr_bytes=$(wc -c < ledgers/PC3/scripts/PC3-a-r4/outputs/twin-$t.stderr)" >> "$OUT"
done
echo DONE >> "$OUT"
