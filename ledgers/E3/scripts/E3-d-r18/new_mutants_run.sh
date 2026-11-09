#!/bin/sh
# Run the round-15 verifier mutants (v15d_01, v15d_02) on seeds 0-9 with the pinned suite. Run from the checkout root.
D=ledgers/E3/scripts/E3-d-r18
R=$(pwd)
for f in ledgers/E3/mutants/v15d_0[12]*.py; do for s in 0 1 2 3 4 5 6 7 8 9; do echo "$f $s"; done; done | \
  xargs -P 14 -n 2 sh -c 'sh '"$D"'/suite_one.sh '"$R"' '"$R"'/$0 $1 | sed "s#^#$0 #"' > $D/new_mutants_seeds_0-9.raw 2>&1
echo DONE > $D/new_mutants.done
