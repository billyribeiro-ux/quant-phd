#!/bin/bash
# SC1-a round 16 gate runs; run from the verifier checkout root; output in out/
cd "$(dirname "$0")/../../../.." || exit 1
O=ledgers/SC1/scripts/SC1-a-r17/out
{ .venv/bin/ruff check . ; echo "rc=$?"; } > $O/ruff_check.out 2>&1
{ .venv/bin/ruff format --check . ; echo "rc=$?"; } > $O/ruff_format.out 2>&1
{ .venv/bin/mypy --no-incremental ; echo "rc=$?"; } > $O/mypy.out 2>&1
{ .venv/bin/pytest -q -k SC1 ; echo "rc=$?"; } > $O/pytest_SC1.out 2>&1
{ .venv/bin/pytest --collect-only -q -k SC1 | tail -3 ; } > $O/collect_SC1.out 2>&1
{ .venv/bin/python tools/check_pages.py --unit SC1 ; echo "rc=$?"; } > $O/check_pages_SC1.out 2>&1
{ .venv/bin/python tools/check_dag.py --unit SC1 ; echo "rc=$?"; } > $O/check_dag_SC1.out 2>&1
{ .venv/bin/python tools/check_projects.py --unit SC1 ; echo "rc=$?"; } > $O/check_projects_SC1.out 2>&1
for p in L01 L02 L03; do { .venv/bin/python tools/run_labs.py --unit SC1 --page $p ; echo "rc=$?"; } > $O/run_labs_$p.out 2>&1; done
for n in 1 2 3; do { .venv/bin/python -I -W error tests/labs/SC1/lab-SC1-L0$n-1.py > $O/twin_L0$n.stdout 2> $O/twin_L0$n.stderr; echo "rc=$?" > $O/twin_L0$n.rc; } ; done
{ .venv/bin/python tools/verify_refs.py --offline ; echo "rc=$?"; } > $O/verify_refs_offline.out 2>&1
{ .venv/bin/python tools/verify_refs.py --unit SC1 ; echo "rc=$?"; } > $O/verify_refs_unit_SC1.out 2>&1
echo DONE > $O/gates_done
