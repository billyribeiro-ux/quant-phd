#!/bin/bash
# Runs every mutant in ledgers/AC1/mutants on seeds 0 and 17; output to out/mutants_r23.out
D=/tmp/verify23-AC1-d/ledgers/AC1/scripts/AC1-d-r23
for f in /tmp/verify23-AC1-d/ledgers/AC1/mutants/*.py; do
  $D/run_one_mutant.sh "$f" /tmp/ac1-v/d23/mut
done > $D/out/mutants_r23.out 2>&1
echo MUTDONE >> $D/out/mutants_r23.out
