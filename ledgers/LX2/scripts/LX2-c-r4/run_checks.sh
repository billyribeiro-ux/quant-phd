#!/bin/bash
# LX2-c round 4: verifier command outputs. Run from the checkout root.
set -u
OUT=ledgers/LX2/scripts/LX2-c-r4/out
PY=.venv/bin/python
{ $PY --version; } > $OUT/python_version.txt 2>&1
$PY tools/check_pages.py --unit LX2 > $OUT/check_pages.txt 2>&1; echo "exit=$?" >> $OUT/check_pages.txt
$PY tools/check_dag.py --unit LX2 > $OUT/check_dag.txt 2>&1; echo "exit=$?" >> $OUT/check_dag.txt
$PY tools/check_projects.py --unit LX2 > $OUT/check_projects.txt 2>&1; echo "exit=$?" >> $OUT/check_projects.txt
$PY tools/run_labs.py --unit LX2 > $OUT/run_labs.txt 2>&1; echo "exit=$?" >> $OUT/run_labs.txt
$PY tools/run_graders.py --unit LX2 > $OUT/run_graders.txt 2>&1; echo "exit=$?" >> $OUT/run_graders.txt
$PY tools/page_smoke.py --unit LX2 --pages project > $OUT/page_smoke_project.txt 2>&1; echo "exit=$?" >> $OUT/page_smoke_project.txt
for t in 1 2 3; do
  $PY -I -W error tests/labs/LX2/lab-LX2-project-$t.py > $OUT/twin-project-$t.txt 2> $OUT/twin-project-$t.err; echo "exit=$?" >> $OUT/twin-project-$t.txt
done
$PY -m ruff check tests/labs/LX2 > $OUT/ruff_check.txt 2>&1; echo "exit=$?" >> $OUT/ruff_check.txt
$PY -m ruff format --check tests/labs/LX2 > $OUT/ruff_format.txt 2>&1; echo "exit=$?" >> $OUT/ruff_format.txt
$PY -m mypy --no-incremental tests/labs/LX2/lab-LX2-project-1.py tests/labs/LX2/lab-LX2-project-2.py tests/labs/LX2/lab-LX2-project-3.py > $OUT/mypy_twins.txt 2>&1; echo "exit=$?" >> $OUT/mypy_twins.txt
