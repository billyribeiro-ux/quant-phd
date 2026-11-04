#!/bin/bash
# Round-6 record script for CS2 slice d: reference / starter / mutants / alternatives over seeds 0-49, collect counts,
# the fuzz of the rank guarantee, and the instance claims. Run from the checkout root.
cd "$(dirname "$0")/../../../.." || exit 1
D=ledgers/CS2/scripts/CS2-d-r6
S=$D/v6_run_suite.sh
OUT=$D/v6_alts_and_refs.out.txt
: > "$OUT"
count_pass() { local f="$1" c=0 s; for s in $(seq 0 49); do o=$($S "$f" $s 2>&1 | tail -1); case "$o" in "174 passed"*) c=$((c+1));; esac; done; echo "$c"; }
echo "reference.py: exactly 174 passed on $(count_pass course/modules/CS/CS2/grader/reference.py)/50 seeds" >> "$OUT"
echo "starter.py seed 0: $($S course/modules/CS/CS2/grader/starter.py 0 2>&1 | tail -1)" >> "$OUT"
for f in $D/alts_v6/*.py ledgers/CS2/equivalent/*.py ledgers/CS2/mutants/v6_0*.py; do
  echo "$(basename $f): exactly 174 passed on $(count_pass $f)/50 seeds" >> "$OUT"
done
.venv/bin/python -I $D/v6_fuzz_sketch.py course/modules/CS/CS2/grader/reference.py ledgers/CS2/equivalent/d8_01_sketch_cap_counts_previous_value.py ledgers/CS2/equivalent/d8_02_sketch_insert_bisect_left.py ledgers/CS2/equivalent/d9_04_sketch_cap_without_plus_one.py $D/alts_v6/alt_v6_d_sketch_never_compresses.py $D/alts_v6/alt_v6_e_sketch_cap_exact_two_epsilon_n.py ledgers/CS2/mutants/v6_03_quantile_target_uses_n_plus_one.py ledgers/CS2/mutants/v6_04_sketch_stores_arrival_order_unsorted.py >> "$OUT" 2>&1
.venv/bin/python -I $D/v6_instance_claims.py course/modules/CS/CS2/grader >> "$OUT" 2>&1
mkdir -p /tmp/v6collect2 && cp course/modules/CS/CS2/grader/instance.py course/modules/CS/CS2/grader/test_project.py course/modules/CS/CS2/grader/reference.py /tmp/v6collect2/ && cp course/modules/CS/CS2/grader/reference.py /tmp/v6collect2/streamstats.py
(cd /tmp/v6collect2 && QF_SEED=0 /Users/billyribeiro/.fanout/wt/verifyD6-CS2-d/.venv/bin/python -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>&1 | tail -1) >> "$OUT"
echo done >> "$OUT"
