#!/bin/bash
# Round 27 command re-runs for AC4-a (checkout root = $1). Each output is saved under out/.
set -u
R="$1"; cd "$R"; P=.venv/bin/python; O=ledgers/AC4/scripts/AC4-a-r27/out
$P tools/check_pages.py --unit AC4 > $O/check_pages.out 2>&1; echo "rc=$?" >> $O/check_pages.out
$P tools/check_dag.py --all > $O/check_dag.out 2>&1; echo "rc=$?" >> $O/check_dag.out
$P tools/check_projects.py --unit AC4 > $O/check_projects.out 2>&1; echo "rc=$?" >> $O/check_projects.out
$P tools/run_labs.py --unit AC4 > $O/run_labs.out 2>&1; echo "rc=$?" >> $O/run_labs.out
$P tools/page_smoke.py --unit AC4 --pages course/modules/AC/AC4/index.html course/modules/AC/AC4/L01.html course/modules/AC/AC4/L02.html > $O/page_smoke.out 2>&1; echo "rc=$?" >> $O/page_smoke.out
$P -I -W error tests/labs/AC4/lab-AC4-L01-1.py > $O/twin_L01.out 2>$O/twin_L01.err; echo "rc=$?" >> $O/twin_L01.out
$P -I -W error tests/labs/AC4/lab-AC4-L02-1.py > $O/twin_L02.out 2>$O/twin_L02.err; echo "rc=$?" >> $O/twin_L02.out
$P tools/verify_refs.py --unit AC4 > $O/verify_refs_live_AC4.out 2>&1; echo "rc=$?" >> $O/verify_refs_live_AC4.out
$P tools/verify_refs.py --offline > $O/verify_refs_offline.out 2>&1; echo "rc=$?" >> $O/verify_refs_offline.out
$P tools/build_site.py --check > $O/build_site_check.out 2>&1; echo "rc=$?" >> $O/build_site_check.out
.venv/bin/pytest -q -k AC4 > $O/pytest_ac4.out 2>&1; echo "rc=$?" >> $O/pytest_ac4.out
.venv/bin/ruff check tests/labs/AC4 > $O/ruff_check.out 2>&1; echo "rc=$?" >> $O/ruff_check.out
.venv/bin/ruff format --check tests/labs/AC4 > $O/ruff_format.out 2>&1; echo "rc=$?" >> $O/ruff_format.out
