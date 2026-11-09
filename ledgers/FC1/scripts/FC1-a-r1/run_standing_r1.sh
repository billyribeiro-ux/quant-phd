#!/bin/bash
# Runs each standing mutant under python -I -W error and compares its stdout with the untouched twin's stdout.
cd /Users/billyribeiro/.fanout/wt/verifyG1-FC1-a || exit 1
S=ledgers/FC1/scripts/FC1-a-r1/out
PY=.venv/bin/python
for t in L01 L02 L03; do $PY -I -W error tests/labs/FC1/lab-FC1-$t-1.py > $S/twin_base_$t.stdout 2>&1; echo "twin $t EXIT=$?"; done
for f in ledgers/FC1/mutants/fc1a-r1/*.py; do
  b=$(basename "$f" .py)
  case "$b" in *L01*) t=L01;; *L02*) t=L02;; *L03*) t=L03;; esac
  $PY -I -W error "$f" > "$S/mut_$b.stdout" 2>&1; e=$?
  if diff -q "$S/twin_base_$t.stdout" "$S/mut_$b.stdout" >/dev/null; then r=SURVIVED; else r=KILLED; fi
  echo "$r EXIT=$e twin=$t $b"
done
