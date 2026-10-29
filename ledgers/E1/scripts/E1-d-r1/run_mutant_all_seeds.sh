#!/bin/bash
# usage: run_mut.sh <mutant.py> ; prints killed-seed count and first killer
P=/tmp/verifyB1-E1-d/.venv/bin/python
m="$1"; name=$(basename "$m" .py); d=/tmp/E1d-v/mut/$name; rm -rf "$d"; mkdir -p "$d"
cp /tmp/E1d-v/ref/test_project.py /tmp/E1d-v/ref/instance.py "$d/"; cp "$m" "$d/market_structure.py"
killed=0; first=""
for s in $(seq 0 49); do
  out=$(cd "$d" && QF_SEED=$s $P -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1)
  if echo "$out" | tail -1 | grep -q failed; then killed=$((killed+1)); [ -z "$first" ] && first="seed $s: $(echo "$out" | grep -m1 '^FAILED' | sed 's/ - .*//')"; fi
done
echo "$name killed_seeds=$killed/50 $first"
