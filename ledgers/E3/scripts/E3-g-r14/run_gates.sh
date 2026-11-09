#!/bin/sh
# Round-14 command rows for E3 slice g (L05-L08). Run from the checkout root.
set -u
PY=.venv/bin/python
OUT=ledgers/E3/scripts/E3-g-r14
for P in L05 L06 L07 L08; do
  $PY tools/run_labs.py --unit E3 --page $P > $OUT/run_labs_$P.out 2>&1; echo "run_labs $P exit $?"
done
$PY tools/check_pages.py --unit E3 > $OUT/check_pages_E3.out 2>&1; echo "check_pages exit $?"
$PY tools/check_dag.py --unit E3 > $OUT/check_dag_E3.out 2>&1; echo "check_dag exit $?"
$PY tools/verify_refs.py --offline --unit E3 > $OUT/verify_refs_E3_offline.out 2>&1; echo "verify_refs exit $?"
$PY -m ruff check . > $OUT/ruff_check.out 2>&1; echo "ruff check exit $?"
$PY -m ruff format --check . > $OUT/ruff_format.out 2>&1; echo "ruff format exit $?"
$PY -m mypy --no-incremental > $OUT/mypy.out 2>&1; echo "mypy exit $?"
