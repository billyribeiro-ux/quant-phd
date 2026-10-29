#!/bin/bash
# Re-runs every earlier alternative (rounds 10 to 21) on seeds 0-49 against the round-23 grader.
D=/tmp/verify23-AC1-d/ledgers/AC1/scripts/AC1-d-r23
{
for f in $(find /tmp/verify23-AC1-d/ledgers/AC1/scripts/AC1-d-r1[0-9]* /tmp/verify23-AC1-d/ledgers/AC1/scripts/AC1-d-r2[01]* -path "*alts*" -name "*.py" | sort); do
  $D/run_alt_one.sh "$f" /tmp/ac1-v/d23/altc
done
echo ALTDONE
} > $D/out/alts_carried_r23.out 2>&1
