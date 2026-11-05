#!/bin/sh
# Run each BK4 lab twin alone under python -I -W error and keep stdout/stderr (round-7 evidence for card numbers).
# Usage (from the checkout root): sh ledgers/BK4/scripts/BK4-d-r7/run_twins_r7.sh
S=ledgers/BK4/scripts/BK4-d-r7/out
mkdir -p $S
for f in tests/labs/BK4/lab-BK4-L01-1.py tests/labs/BK4/lab-BK4-L02-1.py tests/labs/BK4/lab-BK4-L03-1.py tests/labs/BK4/lab-BK4-L04-1.py tests/labs/BK4/lab-BK4-L05-1.py; do
  b=$(basename $f .py)
  python3 -I -W error $f > $S/$b.stdout 2> $S/$b.stderr
  echo "$b exit $? stderr_bytes $(wc -c < $S/$b.stderr)"
done
