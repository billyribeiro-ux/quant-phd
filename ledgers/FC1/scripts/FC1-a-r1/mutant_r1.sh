#!/bin/bash
# Round-1 standing lab-claim mutants (ruling 37): each mutant twin is run alone under python -I -W error
# and its stdout is compared with the unmutated twin stdout. A mutant is killed when the stdout differs.
cd /Users/billyribeiro/.fanout/wt/verifyF11-FC1-a || exit 1
OUT=ledgers/FC1/scripts/FC1-a-r1/out
for m in ledgers/FC1/lab-mutants/*.py; do
  name=$(basename "$m" .py)
  case "$name" in *_L01_*) twin=tests/labs/FC1/lab-FC1-L01-1.py;; *_L02_*) twin=tests/labs/FC1/lab-FC1-L02-1.py;; *_L03_*) twin=tests/labs/FC1/lab-FC1-L03-1.py;; esac
  .venv/bin/python -I -W error "$twin" > "$OUT/mut_base_$name.out" 2>&1; eb=$?
  .venv/bin/python -I -W error "$m" > "$OUT/mut_$name.out" 2>&1; em=$?
  if diff -q "$OUT/mut_base_$name.out" "$OUT/mut_$name.out" >/dev/null; then k=SURVIVED; else k=KILLED; fi
  echo "$k base_exit=$eb mutant_exit=$em $name twin=$twin"
  diff "$OUT/mut_base_$name.out" "$OUT/mut_$name.out" | head -6
done
