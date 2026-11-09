#!/bin/bash
cd /Users/billyribeiro/.fanout/wt/verifyF31-PC3-c || exit 1
S=ledgers/PC3/scripts/PC3-c-r1
MODS=()
while IFS= read -r line; do MODS+=("$line"); done < ledgers/PC3/scripts/PC3-c-r18/out/candidate_modules_r18.txt
echo "# ${#MODS[@]} prior candidate modules, seed 0"
$S/run_candidates_r1.sh 0 "${MODS[@]}"
echo "# ${#MODS[@]} prior candidate modules, seed 77314143"
$S/run_candidates_r1.sh 77314143 "${MODS[@]}"
