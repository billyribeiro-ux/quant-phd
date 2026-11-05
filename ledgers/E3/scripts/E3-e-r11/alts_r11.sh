#!/bin/bash
# Runs the grader suite on seeds 0-9 with each alternative correct implementation as elicit.py (test-only fixture).
ROOT=/Users/billyribeiro/.fanout/wt/verifyD11-E3-e
PY=$ROOT/.venv/bin/python
OUT=$ROOT/ledgers/E3/scripts/E3-e-r11/out/alts
mkdir -p $OUT
for alt in alt1_grid_zoom_newton alt2_pure_newton_fd1e-6 alt3_nelder_mead alt4_bisection_ce alt5_exp_log_float; do
  W=/tmp/e3e_r11/ws_$alt
  rm -rf $W; mkdir -p $W
  cp $ROOT/course/modules/E/E3/grader/test_project.py $ROOT/course/modules/E/E3/grader/instance.py $W/
  cp $ROOT/ledgers/E3/scripts/E3-d-r10/alts/$alt/elicit.py $W/elicit.py
  for s in 0 1 2 3 4 5 6 7 8 9; do
    ( cd $W && QF_SEED=$s $PY -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > $OUT/${alt}_seed$s.txt 2>&1; echo "seed $s exit $?" >> $OUT/${alt}_seed$s.txt )
  done
  echo "$alt: $(for s in 0 1 2 3 4 5 6 7 8 9; do tail -1 $OUT/${alt}_seed$s.txt | awk '{printf "%s ", $0}'; done)" >> $OUT/summary.txt
done
echo DONE >> $OUT/summary.txt
