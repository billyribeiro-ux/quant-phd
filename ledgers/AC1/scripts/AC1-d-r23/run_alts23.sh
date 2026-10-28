#!/bin/bash
# Runs the three round-23 alternatives and the three round-22 alternatives on seeds 0-49.
D=/tmp/verify23-AC1-d/ledgers/AC1/scripts/AC1-d-r23
{
for f in /tmp/ac1-v/d23/alts/*.py /tmp/verify23-AC1-d/ledgers/AC1/scripts/AC1-d-r22/alts/*.py; do
  $D/run_alt_one.sh "$f" /tmp/ac1-v/d23/alt
done
echo ALTDONE
} > $D/out/alts_r23.out 2>&1
