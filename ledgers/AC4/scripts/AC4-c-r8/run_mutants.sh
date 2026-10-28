#!/bin/sh
# usage: run_mutants.sh <checkout> ; each mutant is run against the twin it differs from, under python -I -W error
CO="$1"; P="$CO/.venv/bin/python"; OUT=/tmp/AC4-v/AC4-c-r8/mut; mkdir -p "$OUT"
L05="$CO/tests/labs/AC4/lab-AC4-L05-1.py"; L06="$CO/tests/labs/AC4/lab-AC4-L06-1.py"
for f in "$CO"/ledgers/AC4/mutants/AC4-c-r8/*.py; do
  b=$(basename "$f")
  if head -1 "$f" | grep -q "L05 lab"; then T="$L05"; else T="$L06"; fi
  "$P" -I -W error "$f" > "$OUT/$b.out" 2>&1; rc=$?
  if [ $rc -ne 0 ]; then st="KILLED(rc=$rc)"; else
    if cmp -s "$OUT/$b.out" "$OUT/baseline_$(basename $T).out"; then st="SURVIVED(same output as twin)"; else st="KILLED(output differs)"; fi
  fi
  echo "$b [$(basename $T)] -> $st : $(tail -1 "$OUT/$b.out" | cut -c1-100)"
done
