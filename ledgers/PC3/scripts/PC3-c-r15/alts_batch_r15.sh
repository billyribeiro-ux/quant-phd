#!/bin/bash
# Runs every alternative correct implementation (alt_candidates.txt) on seeds 0-49 against the pinned grader.
cd /Users/billyribeiro/.fanout/wt/verifyE15-PC3-c
S=ledgers/PC3/scripts/PC3-c-r15
mkdir -p $S/out/alts
one() {
  f="$1"; name=$(basename "$f" .py)
  .venv/bin/python -I $S/run_cand_r15.py "$f" range > "$S/out/alts/$name.txt" 2>&1
  echo "$name pass=$(grep -c 'exit=0' "$S/out/alts/$name.txt") of=$(wc -l < "$S/out/alts/$name.txt")" >> $S/out/alts/SUMMARY.txt
}
export -f one; export S
rm -f $S/out/alts/SUMMARY.txt
cat $S/alt_candidates.txt | xargs -P 6 -I{} bash -c 'one "$@"' _ {}
echo ALTS_DONE >> $S/out/alts/SUMMARY.txt
