#!/bin/sh
# Gates for E3 slice g (cards of L05-L08), run from the checkout root with the checkout's .venv.
set -u
S=ledgers/E3/scripts/E3-g-r3
PY=.venv/bin/python
for L in L05 L06 L07 L08; do $PY tools/check_pages.py --unit E3 --page $L; echo "exit=$?"; done
$PY tools/check_pages.py --unit E3; echo "exit=$?"
$PY tools/check_dag.py --unit E3; echo "exit=$?"
$PY tools/check_projects.py --unit E3; echo "exit=$?"
$PY tools/run_labs.py --unit E3; echo "exit=$?"
for L in 05 06 07 08; do $PY -I -W error tests/labs/E3/lab-E3-L$L-1.py > $S/twin_L$L.r3.out 2> $S/twin_L$L.r3.err; echo "twin L$L exit=$?"; done
$PY tools/page_smoke.py --unit E3 --pages L05 L06 L07 L08; echo "exit=$?"
$PY tools/verify_refs.py --offline; echo "exit=$?"
.venv/bin/ruff check tests/labs/E3/lab-E3-L05-1.py tests/labs/E3/lab-E3-L06-1.py tests/labs/E3/lab-E3-L07-1.py tests/labs/E3/lab-E3-L08-1.py; echo "ruff exit=$?"
