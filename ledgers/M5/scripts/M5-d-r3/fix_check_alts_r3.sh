#!/bin/bash
# Round 3, slice d: the five alternatives against the patched COPY of the suite (scratch) on seeds 0-9.
R=/Users/billyribeiro/.fanout/wt/verifyS3-M5-d
W=/tmp/m5d_r3_fix/patched
for c in alt1_functional_reduce_and_tuples alt2_class_with_precomputed_feasible_tables alt3_comprehension_with_feasible_index_lists alt4_bisect_for_feasible_successors alt5_reverse_order_synchronous_sweep; do
  cp $R/ledgers/M5/alternatives/$c.py $W/contraction_solver.py
  res=""
  for s in 0 1 2 3 4 5 6 7 8 9; do
    if (cd $W && QF_SEED=$s PYTHONHASHSEED=0 $R/.venv/bin/python -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1); then res="$res $s:P"; else res="$res $s:F"; fi
  done
  echo "patched suite, $c:$res"
done
