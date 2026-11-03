#!/bin/sh
# E3 slice f round 4: the gate commands this slice relies on, run from the checkout root. Outputs go next to this file.
set -u
cd "$(dirname "$0")/../../../.." || exit 1
D=ledgers/E3/scripts/E3-f-r4
.venv/bin/python tools/check_pages.py --unit E3 > $D/check_pages.out 2>&1; echo "check_pages exit=$?" >> $D/check_pages.out
.venv/bin/python tools/check_dag.py --unit E3 > $D/check_dag.out 2>&1; echo "check_dag exit=$?" >> $D/check_dag.out
.venv/bin/python tools/check_projects.py --unit E3 > $D/check_projects.out 2>&1; echo "check_projects exit=$?" >> $D/check_projects.out
for p in L01 L02 L03 L04; do .venv/bin/python tools/run_labs.py --unit E3 --page $p; done > $D/run_labs_L01-L04.out 2>&1
for t in L01 L02 L03 L04; do
  .venv/bin/python -I -W error tests/labs/E3/lab-E3-$t-1.py > $D/twins/$t.out 2> $D/twins/$t.err
  echo "$t twin exit=$? stderr_bytes=$(wc -c < $D/twins/$t.err)"
done > $D/twins/summary.out
.venv/bin/python -I $D/diff_expected_r4.py > $D/twins/expected_vs_twin.out 2>&1
.venv/bin/python tools/page_smoke.py --unit E3 --pages L01 L02 L03 L04 > $D/page_smoke_L01-L04.out 2>&1; echo "page_smoke exit=$?" >> $D/page_smoke_L01-L04.out
.venv/bin/pytest tests/test_labs.py -q -k E3 > $D/pytest_labs_E3.out 2>&1; echo "pytest exit=$?" >> $D/pytest_labs_E3.out
.venv/bin/python tools/verify_refs.py --offline > $D/verify_refs_offline.out 2>&1; echo "verify_refs exit=$?" >> $D/verify_refs_offline.out
