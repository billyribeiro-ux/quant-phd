#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyF31-PC3-c || exit 1
S=ledgers/PC3/scripts/PC3-c-r1
MODS=(ledgers/PC3/scripts/PC3-c-r18/alt_r18_1_skew_and_size.py ledgers/PC3/scripts/PC3-c-r18/alt_r18_2_mean_of_last_three_fills.py ledgers/PC3/scripts/PC3-c-r18/alt_r18_3_never_quotes.py ledgers/PC3/mutants/r18_01_replay_resimulates_the_game_from_the_seed.py ledgers/PC3/mutants/r18_02_replay_books_informed_fills_as_purchases.py ledgers/PC3/mutants/r18_03_replay_marks_the_change_from_the_start_value.py course/modules/PC/PC3/grader/reference.py course/modules/PC/PC3/grader/starter.py)
echo '$ run_candidates_r1.sh 0 <r18 alts, r18 mutants, reference, starter>'
$S/run_candidates_r1.sh 0 "${MODS[@]}"
echo '$ run_candidates_r1.sh 77314143 <same>'
$S/run_candidates_r1.sh 77314143 "${MODS[@]}"
