#!/bin/sh
# Run the five round-14 verifier alternatives on seeds 0-9 with the current grader. Run from the checkout root.
D=ledgers/E3/scripts/E3-d-r15/verifier
R=$(pwd)
for a in 1 2 3 4 5; do for s in 0 1 2 3 4 5 6 7 8 9; do echo "$a $s"; done; done | \
  xargs -P 12 -n 2 sh -c 'sh '"$D"'/suite_one.sh '"$R"' '"$R"'/ledgers/E3/scripts/E3-d-r14/alts/alt_v$0/elicit.py $1 | sed "s/^/alt_v$0 /"' > $D/alternatives_seeds_0-9.raw 2>&1
echo DONE > $D/alternatives.done
