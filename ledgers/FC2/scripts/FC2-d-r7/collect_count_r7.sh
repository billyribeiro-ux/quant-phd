#!/bin/bash
# Collect-only count per seed on the reference solution (copied as scanner.py in a scratch dir).
set -u
D="$1"; V="$2"
for s in $(seq 0 49); do
  n=$(cd "$D" && QF_SEED=$s "$V" -I -m pytest --collect-only -q -p no:cacheprovider test_project.py 2>/dev/null | tail -1)
  echo "seed $s $n"
done
