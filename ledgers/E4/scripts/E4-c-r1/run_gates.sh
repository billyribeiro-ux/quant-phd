#!/bin/bash
# E4-c round 1 command rows. Run from the checkout root.
set -u
O=ledgers/E4/scripts/E4-c-r1/out
PY=.venv/bin/python
for p in L07 L08 L09; do $PY tools/check_pages.py --unit E4 --page $p > $O/check_pages_$p.out 2>&1; echo "check_pages $p exit=$?" >> $O/summary.out; done
$PY tools/check_dag.py --unit E4 > $O/check_dag.out 2>&1; echo "check_dag exit=$?" >> $O/summary.out
$PY tools/check_projects.py --unit E4 > $O/check_projects.out 2>&1; echo "check_projects exit=$?" >> $O/summary.out
for p in L07 L08 L09; do $PY tools/run_labs.py --unit E4 --page $p > $O/run_labs_$p.out 2>&1; echo "run_labs $p exit=$?" >> $O/summary.out; done
$PY tools/mutate_graders.py --help > $O/mutate_help.out 2>&1
