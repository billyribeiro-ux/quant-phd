#!/bin/sh
# LX1 slice a, closing delta round 1 (pin 95f3f8cb, base fragment pin 67a2d13e). Run from the checkout root; outputs in out-delta/.
set -u
P=.venv/bin/python
S=ledgers/LX1/scripts/LX1-a-r1/out-delta
$P tools/check_pages.py --unit LX1 > $S/check_pages.txt 2>&1; echo "check_pages exit $?"
$P tools/check_dag.py --unit LX1 > $S/check_dag.txt 2>&1; echo "check_dag exit $?"
$P tools/check_projects.py --unit LX1 > $S/check_projects.txt 2>&1; echo "check_projects exit $?"
$P tools/run_labs.py --unit LX1 > $S/run_labs_unit.txt 2>&1; echo "run_labs exit $?"
$P -I -W error tests/labs/LX1/lab-LX1-L01-1.py > $S/twin_L01.out 2> $S/twin_L01.err; echo "twin L01 exit $?"
$P -I -W error tests/labs/LX1/lab-LX1-L02-1.py > $S/twin_L02.out 2> $S/twin_L02.err; echo "twin L02 exit $?"
$P -I ledgers/LX1/scripts/LX1-a-r1/page_twin_check.py "$PWD" > $S/page_twin_check.txt 2>&1; echo "page_twin_check exit $?"
$P -I ledgers/LX1/scripts/LX1-a-r1/numbers_r1.py > $S/numbers_r1.txt 2>&1; echo "numbers_r1 exit $?"
$P tools/page_smoke.py --unit LX1 --pages index L01 L02 > $S/page_smoke_index_L01_L02.txt 2>&1; echo "page_smoke exit $?"
.venv/bin/ruff check tests/labs/LX1/lab-LX1-L01-1.py tests/labs/LX1/lab-LX1-L02-1.py > $S/ruff_twins.txt 2>&1; echo "ruff check exit $?"
.venv/bin/ruff format --check tests/labs/LX1/lab-LX1-L01-1.py tests/labs/LX1/lab-LX1-L02-1.py >> $S/ruff_twins.txt 2>&1; echo "ruff format exit $?"
.venv/bin/mypy --no-incremental tests/labs/LX1/lab-LX1-L01-1.py tests/labs/LX1/lab-LX1-L02-1.py > $S/mypy_twins.txt 2>&1; echo "mypy exit $?"
.venv/bin/pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_docs_figures.py -k "LX1 or lx1 or L01 or L02 or twin or lab or docs or page" -p no:cacheprovider > $S/pytest_subset.txt 2>&1; echo "pytest subset exit $?"
$P tools/verify_refs.py --offline > $S/verify_refs_offline.txt 2>&1; echo "verify_refs offline exit $?"
$P tools/fetch_data.py --check > $S/fetch_data_check.txt 2>&1; echo "fetch_data check exit $?"
$P tools/mutate_graders.py --unit LX1 > $S/mutate_graders_LX1.txt 2>&1; echo "mutate_graders exit $?"
$P tools/run_graders.py --unit LX1 > $S/run_graders_LX1.txt 2>&1; echo "run_graders exit $?"
