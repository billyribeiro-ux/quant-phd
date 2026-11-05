#!/bin/bash
# Round-9 key candidate runs saved to out/ so every cited output exists. Usage: bash key_runs_r9.sh (from anywhere)
ROOT=/Users/billyribeiro/.fanout/wt/verifyE9-SC1-d
R=$ROOT/ledgers/SC1/scripts/SC1-d-r9
PY=$ROOT/.venv/bin/python
cd $ROOT
: > $R/out/reference_seeds_0_9_r9.txt
for s in 0 1 2 3 4 5 6 7 8 9; do $PY -I $R/run_candidate.py course/modules/SC/SC1/grader/reference.py $s 120 | head -1 >> $R/out/reference_seeds_0_9_r9.txt; done
$PY -I $R/run_candidate.py ledgers/SC1/mutants/r8_07_bruteforce_walk_listing.py 0 120 > $R/out/r8_07_seed0_r9.txt
$PY -I $R/run_candidate.py ledgers/SC1/mutants/r8_01_leftover_print_on_boundary_walk.py 0 120 > $R/out/r8_01_seed0_r9.txt
$PY -I $R/run_candidate.py ledgers/SC1/mutants/r8_06_leftover_print_for_two_paths.py 0 120 > $R/out/r8_06_seed0_r9.txt
TEST_FILE=/tmp/sc1d-r9-work/fixcheck/test_project_fixed2.py $PY -I $R/run_candidate.py course/modules/SC/SC1/grader/reference.py 0 120 > $R/out/fixed2_reference_seed0_r9.txt
echo done
