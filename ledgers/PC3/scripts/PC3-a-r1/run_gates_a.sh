#!/bin/sh
# Round-1 slice a gate commands for PC3 (hub, L01-L03, lab twins). Run from the checkout root.
# Each command was run by the verifier at pin 1c1645f; outputs are summarised in ledgers/PC3/PC3-a.json.
set -u
PY=.venv/bin/python
$PY tools/check_pages.py --unit PC3 --page L01
$PY tools/check_pages.py --unit PC3 --page L02
$PY tools/check_pages.py --unit PC3 --page L03
$PY tools/check_pages.py --unit PC3
$PY tools/check_dag.py --unit PC3
$PY tools/check_projects.py --unit PC3
$PY tools/run_labs.py --unit PC3 --page L01
$PY tools/run_labs.py --unit PC3 --page L02
$PY tools/run_labs.py --unit PC3 --page L03
for n in L01-1 L02-1 L03-1; do
  (cd "$(mktemp -d)" && "$OLDPWD/$PY" -I -W error "$OLDPWD/tests/labs/PC3/lab-PC3-$n.py" >/dev/null) || echo "twin $n failed"
done
$PY tools/page_smoke.py --unit PC3 --pages index L01 L02 L03
.venv/bin/ruff check tests/labs/PC3 && .venv/bin/ruff format --check tests/labs/PC3
.venv/bin/mypy --no-incremental tests/labs/PC3
.venv/bin/pytest tests/test_labs.py -k PC3 -q
$PY tools/verify_refs.py --offline
$PY tools/verify_refs.py --unit PC3
$PY ledgers/PC3/scripts/PC3-a-r1/recompute_a.py
