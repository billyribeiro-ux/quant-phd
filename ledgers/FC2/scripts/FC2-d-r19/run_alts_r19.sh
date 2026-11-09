#!/bin/bash
# Runs each correct alternative as scanner.py against the current FC2 grader, seeds 0-49, same flags as run_graders.
ROOT=/Users/billyribeiro/.fanout/wt/verifyD19-FC2-d
S=$ROOT/ledgers/FC2/scripts/FC2-d-r19
G=$ROOT/course/modules/FC/FC2/grader
PY=$ROOT/.venv/bin/python
ALTS="$ROOT/ledgers/FC2/scripts/FC2-d-r14/alts/alt1_fraction_class.py $ROOT/ledgers/FC2/scripts/FC2-d-r14/alts/alt2_integer_only.py $ROOT/ledgers/FC2/scripts/FC2-d-r14/alts/alt3_float_epsilon_cutoff.py $ROOT/ledgers/FC2/scripts/FC2-d-r14/alts/alt4_adjacent_slopes.py $ROOT/ledgers/FC2/scripts/FC2-d-r14/alts/alt5_forward_price_parity.py $ROOT/ledgers/FC2/scripts/FC2-d-r14/alt6_round6_alternative.py $ROOT/ledgers/FC2/scripts/FC2-d-r15/alts/alt7_integer_scaled.py $ROOT/ledgers/FC2/scripts/FC2-d-r15/alts/alt8_decimal_60.py"
for a in $ALTS; do
  n=$(basename $a .py)
  W=$S/alt_stage/$n; rm -rf $W; mkdir -p $W
  cp $G/test_project.py $G/instance.py $W/; cp $a $W/scanner.py
  fails=0; pass=0
  for s in $(seq 0 49); do
    if (cd $W && QF_SEED=$s PYTHONHASHSEED=0 $PY -I -m pytest -q -p no:cacheprovider -W error test_project.py >/dev/null 2>&1); then pass=$((pass+1)); else fails=$((fails+1)); fi
  done
  echo "$n pass=$pass fail=$fails"
done
