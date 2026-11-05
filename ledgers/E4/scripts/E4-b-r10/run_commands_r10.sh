#!/bin/sh
# E4-b round-10 verifier: the gate commands run against the pin 00a84795 (outputs under outputs/).
# Run from the checkout root. Each command's exact output is in outputs/ with the name shown.
set -u
PY=.venv/bin/python
O=ledgers/E4/scripts/E4-b-r10/outputs
$PY tools/check_pages.py --unit E4 > $O/check_pages_E4.txt 2>&1; echo "exit $?" >> $O/check_pages_E4.txt
for p in L04 L05 L06; do $PY tools/check_pages.py --unit E4 --page $p > $O/check_pages_$p.txt 2>&1; echo "exit $?" >> $O/check_pages_$p.txt; done
$PY tools/check_dag.py --unit E4 > $O/check_dag_E4.txt 2>&1; echo "exit $?" >> $O/check_dag_E4.txt
$PY tools/check_dag.py --all > $O/check_dag_all.txt 2>&1; echo "exit $?" >> $O/check_dag_all.txt
$PY tools/check_projects.py --unit E4 > $O/check_projects_E4.txt 2>&1; echo "exit $?" >> $O/check_projects_E4.txt
$PY tools/run_labs.py --unit E4 > $O/run_labs_E4.txt 2>&1; echo "exit $?" >> $O/run_labs_E4.txt
for t in L04 L05 L06; do
  (cd tests/labs/E4 && $PY -I -W error lab-E4-$t-1.py > $OLDPWD/$O/twin_$t.txt 2> $OLDPWD/$O/twin_${t}_stderr.txt; echo "exit $?" >> $OLDPWD/$O/twin_$t.txt)
done
$PY -I ledgers/E4/scripts/E4-b-r10/page_twin_check.py > $O/page_twin_check.txt
$PY -m ruff check tests/labs/E4/lab-E4-L04-1.py tests/labs/E4/lab-E4-L05-1.py tests/labs/E4/lab-E4-L06-1.py > $O/ruff_check.txt 2>&1; echo "exit $?" >> $O/ruff_check.txt
$PY -m ruff format --check tests/labs/E4/lab-E4-L04-1.py tests/labs/E4/lab-E4-L05-1.py tests/labs/E4/lab-E4-L06-1.py > $O/ruff_format.txt 2>&1; echo "exit $?" >> $O/ruff_format.txt
$PY -m ruff check . > $O/ruff_repo.txt 2>&1; echo "exit $?" >> $O/ruff_repo.txt
$PY -m mypy --no-incremental tests/labs/E4/lab-E4-L04-1.py tests/labs/E4/lab-E4-L05-1.py tests/labs/E4/lab-E4-L06-1.py > $O/mypy_twins.txt 2>&1; echo "exit $?" >> $O/mypy_twins.txt
$PY -m mypy --no-incremental > $O/mypy_full.txt 2>&1; echo "exit $?" >> $O/mypy_full.txt
$PY -m pytest tests/test_labs.py tests/test_run_labs.py -p no:cacheprovider -o addopts="" -rA > $O/pytest_labs_full.txt 2>&1; echo "exit $?" >> $O/pytest_labs_full.txt
$PY -m pytest tests/test_page_checks.py tests/test_page_smoke.py -p no:cacheprovider -o addopts="" -rA > $O/pytest_page_checks.txt 2>&1; echo "exit $?" >> $O/pytest_page_checks.txt
$PY tools/page_smoke.py --unit E4 --pages L04 L05 L06 > $O/page_smoke_E4.txt 2>&1; echo "exit $?" >> $O/page_smoke_E4.txt
$PY tools/verify_refs.py --offline > $O/verify_refs_offline.txt 2>&1; echo "exit $?" >> $O/verify_refs_offline.txt
$PY tools/verify_refs.py --unit E4 > $O/verify_refs_unit_E4_live.txt 2>&1; echo "exit $?" >> $O/verify_refs_unit_E4_live.txt
$PY tools/render_curriculum.py > $O/render.txt 2>&1; echo "exit $?" >> $O/render.txt
git diff --exit-code -- CURRICULUM.md curriculum/curriculum.json > $O/render_diff.txt 2>&1; echo "exit $?" >> $O/render_diff.txt
$PY -I $S/rederive_r10.py > $O/rederive_r10.txt
$PY -I $S/structure_scan_r10.py > $O/structure_scan_r10.txt
# Muth record: plain curl, no personal data in the request
curl -s -m 30 -o $O/crossref_muth.json -w "HTTP %{http_code}\n" "https://api.crossref.org/works/10.2307/1909635"
