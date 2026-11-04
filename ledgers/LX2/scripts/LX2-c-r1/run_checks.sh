#!/bin/sh
# LX2 slice c, round 1: re-run the checks behind the project.html rows. Run from the checkout root:
#   sh ledgers/LX2/scripts/LX2-c-r1/run_checks.sh
# Outputs go to ledgers/LX2/scripts/LX2-c-r1/out/.
set -u
D=ledgers/LX2/scripts/LX2-c-r1
O=$D/out
PY=.venv/bin/python
$PY tools/check_projects.py --unit LX2 > $O/check_projects.txt 2>&1; echo "check_projects exit $?" >> $O/check_projects.txt
$PY tools/check_pages.py --unit LX2 > $O/check_pages.txt 2>&1; echo "check_pages exit $?" >> $O/check_pages.txt
$PY tools/check_dag.py --unit LX2 > $O/check_dag.txt 2>&1; echo "check_dag exit $?" >> $O/check_dag.txt
$PY tools/run_labs.py --unit LX2 > $O/run_labs.txt 2>&1; echo "run_labs exit $?" >> $O/run_labs.txt
$PY tools/page_smoke.py --unit LX2 --pages project > $O/page_smoke_project.txt 2>&1; echo "page_smoke exit $?" >> $O/page_smoke_project.txt
$PY tools/verify_refs.py --unit LX2 > $O/verify_refs_unit.txt 2>&1; echo "verify_refs exit $?" >> $O/verify_refs_unit.txt
$PY tools/run_graders.py --unit LX2 > $O/run_graders.txt 2>&1; echo "run_graders exit $?" >> $O/run_graders.txt
for n in 1 2 3; do python3 -I -W error tests/labs/LX2/lab-LX2-project-$n.py > $O/twin-project-$n.txt 2>&1; echo "exit $?" >> $O/twin-project-$n.txt; done
python3 -I -W error $D/page_vs_twin.py > $O/page_vs_twin.txt 2>&1; echo "exit $?" >> $O/page_vs_twin.txt
python3 -I -W error $D/recompute_project_numbers.py > $O/recompute_project_numbers.txt 2>&1
python3 -I -W error $D/lab2_mutants.py > $O/lab2_mutants.txt 2>&1; echo "exit $?" >> $O/lab2_mutants.txt
.venv/bin/ruff check tests/labs/LX2/lab-LX2-project-1.py tests/labs/LX2/lab-LX2-project-2.py tests/labs/LX2/lab-LX2-project-3.py > $O/ruff.txt 2>&1; echo "exit $?" >> $O/ruff.txt
.venv/bin/mypy --no-incremental tests/labs/LX2/lab-LX2-project-1.py tests/labs/LX2/lab-LX2-project-2.py tests/labs/LX2/lab-LX2-project-3.py > $O/mypy.txt 2>&1; echo "exit $?" >> $O/mypy.txt
.venv/bin/pytest -q -k LX2 tests/test_labs.py tests/test_page_checks.py tests/test_run_labs.py > $O/pytest_lx2.txt 2>&1; echo "exit $?" >> $O/pytest_lx2.txt
curl -sS -L --max-time 60 -A "Mozilla/5.0" -o $O/sr2602.htm -w "HTTP %{http_code} bytes %{size_download}\n" https://www.federalreserve.gov/supervisionreg/srletters/sr2602.htm > $O/sr2602_fetch.txt 2>&1
