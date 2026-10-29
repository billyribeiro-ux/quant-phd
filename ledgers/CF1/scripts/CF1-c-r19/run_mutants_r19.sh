#!/bin/sh
# Round 19: run every lab-twin mutant and alternative against the current twins (python -I -W error).
# Usage: run_mutants_r19.sh <checkout> <outdir>
CK=$1; OUT=$2; P=$CK/.venv/bin/python
mkdir -p "$OUT"
for f in "$CK"/ledgers/CF1/scripts/CF1-c-r18/mutants/*.py "$CK"/ledgers/CF1/scripts/CF1-c-r17/mutants/*.py; do
  b=$(basename "$f" .py)
  case "$b" in *L06*) base=lab-CF1-L06-1;; *) base=lab-CF1-L05-1;; esac
  "$P" -I -W error "$f" > "$OUT/$b.out" 2> "$OUT/$b.err"; rc=$?
  if [ "$b" = "$b" ]; then :; fi
  echo "$b rc=$rc lines=$(wc -l < "$OUT/$b.out")"
done
