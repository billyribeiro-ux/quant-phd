#!/bin/sh
# Verifier round 15, slice e (E3 hub and lessons L01-L08). Run from the checkout root.
# Writes out/gates.out. Commands are the gate runs cited by the fragment rows.
cd "$(dirname "$0")/../../../.." || exit 1
O=ledgers/E3/scripts/E3-e-r15/out
P=.venv/bin/python
{
echo "## check_pages E3"; $P tools/check_pages.py --unit E3; echo "exit $?";
echo "## check_dag E3"; $P tools/check_dag.py --unit E3; echo "exit $?";
for n in 1 2 3 4 5 6 7 8; do echo "## run_labs E3 L0$n"; $P tools/run_labs.py --unit E3 --page L0$n; echo "exit $?"; done;
echo "## page_smoke E3 pages"; $P tools/page_smoke.py --unit E3 --pages index L01 L02 L03 L04 L05 L06 L07 L08; echo "exit $?";
for n in 1 2 3 4 5 6 7 8; do echo "## twin L0$n"; $P -I -W error tests/labs/E3/lab-E3-L0$n-1.py > /tmp/e3e_r15_twin$n.txt 2>&1; echo "exit $?"; md5sum /tmp/e3e_r15_twin$n.txt; done;
echo "## verify_refs offline"; $P tools/verify_refs.py --offline; echo "exit $?";
echo "## ruff"; .venv/bin/ruff check . ; echo "exit $?"; .venv/bin/ruff format --check . ; echo "exit $?";
echo "## mypy"; .venv/bin/mypy --no-incremental; echo "exit $?";
echo "## pytest relevant"; $P -m pytest -q tests/test_labs.py tests/test_run_labs.py tests/test_page_checks.py tests/test_build_site.py tests/test_docs_figures.py tests/test_page_smoke.py tests/test_curriculum.py; echo "exit $?";
echo "## check_projects E3 (unit gate; not slice e content)"; $P tools/check_projects.py --unit E3; echo "exit $?";
} > $O/gates.out 2>&1
