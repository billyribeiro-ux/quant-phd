#!/bin/bash
# PC3 slice a, round 8 verifier gates. Run from the checkout root.
set -u
cd /Users/billyribeiro/.fanout/wt/verifyE8-PC3-a || exit 1
OUT=ledgers/PC3/scripts/PC3-a-r8/outputs
PY=.venv/bin/python
run() { name="$1"; shift; { echo "\$ $*"; "$@"; echo "exit=$?"; } > "$OUT/$name.out" 2>&1; echo "$name: $(tail -1 "$OUT/$name.out")"; }
run check_pages $PY tools/check_pages.py --unit PC3
run check_dag $PY tools/check_dag.py --unit PC3
run check_projects $PY tools/check_projects.py --unit PC3
run run_labs_all $PY tools/run_labs.py --unit PC3
run run_labs_L01 $PY tools/run_labs.py --unit PC3 --page L01
run run_labs_L02 $PY tools/run_labs.py --unit PC3 --page L02
run run_labs_L03 $PY tools/run_labs.py --unit PC3 --page L03
for t in L01 L02 L03; do run twin_$t $PY -I -W error tests/labs/PC3/lab-PC3-$t-1.py; done
run ruff_check .venv/bin/ruff check tests/labs/PC3 tools
run ruff_format .venv/bin/ruff format --check tests/labs/PC3
run mypy_twins .venv/bin/mypy --no-incremental
run pytest_labs_PC3 .venv/bin/pytest tests/test_labs.py -k PC3 -q
run pytest_collect_PC3 .venv/bin/pytest tests/test_labs.py -k PC3 --collect-only -q
run verify_refs_offline $PY tools/verify_refs.py --offline
run page_smoke_slice $PY tools/page_smoke.py --unit PC3 --pages index L01 L02 L03
