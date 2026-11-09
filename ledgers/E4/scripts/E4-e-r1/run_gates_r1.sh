#!/bin/bash
# Round-1 closing-delta gates for E4 slice e, run from the verifier checkout (pin 95f3f8cb).
cd /Users/billyribeiro/.fanout/wt/verifyF31-E4-e || exit 1
OUT=ledgers/E4/scripts/E4-e-r1/outputs
PY=.venv/bin/python
run() { name="$1"; shift; "$@" > "$OUT/$name.txt" 2>&1; echo "$name exit $?" >> "$OUT/exit_codes.txt"; }
: > "$OUT/exit_codes.txt"
run check_pages $PY tools/check_pages.py --unit E4
run check_dag $PY tools/check_dag.py --unit E4
run check_projects $PY tools/check_projects.py --unit E4
run verify_refs_offline $PY tools/verify_refs.py --offline
run run_labs $PY tools/run_labs.py --unit E4
run page_smoke_all_lessons $PY tools/page_smoke.py --unit E4 --pages L01 L02 L03 L04 L05 L06 L07 L08 L09 --skip-sweep
for t in L01 L02 L03 L04 L05 L06 L07 L08 L09; do
  run twin_$t env -i PATH=/usr/bin:/bin $PY -I -W error tests/labs/E4/lab-E4-$t-1.py
done
