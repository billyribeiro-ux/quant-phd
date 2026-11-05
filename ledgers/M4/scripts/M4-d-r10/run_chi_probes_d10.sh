#!/bin/bash
# Round-10 verifier D: for each chi-square sharing probe, run the M4 chi-square lag test on seeds 0-49 (QF_SEED).
PY=/Users/billyribeiro/.fanout/wt/verifyD10-M4-d/.venv/bin/python
cd /Users/billyribeiro/.fanout/wt/verifyD10-M4-d/ledgers/M4/scripts/M4-d-r10/probes || exit 1
for mode in ref lag1_pairs_2k_2k1 lag2_pairs_4j_4j2 lag3_pairs_6j_6j3 even_all_share chain_lag4_4j_4j4 disjoint_lag4_8j_8j4; do
  for s in $(seq 0 49); do
    echo "$mode $s"
  done
done | xargs -P 8 -n 2 sh -c 'cd "'"$PWD"'"/$0 && r=$(QF_SEED=$1 '"$PY"' -m pytest -q -p no:cacheprovider --assert=plain -W error -k test_student_t_draws_do_not_share_chi_square test_project.py 2>&1 | tail -1); case "$r" in *failed*) v=FAIL;; *passed*) v=PASS;; *) v=ERR;; esac; echo "$0 seed=$1 $v"'
