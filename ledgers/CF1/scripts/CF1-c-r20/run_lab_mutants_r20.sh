#!/bin/sh
# Round 20: run every lab-twin mutant (r17, r18) and alternative against the current twins under python -I -W error.
# Usage: run_lab_mutants_r20.sh <checkout> <outdir>
CK=$1; OUT=$2; P=$CK/.venv/bin/python
mkdir -p "$OUT"
for L in L05 L06; do
  base="$CK/tests/labs/CF1/lab-CF1-$L-1.py"
  "$P" -I -W error "$base" > "$OUT/base_$L.out" 2>&1; echo "base $L rc=$?"
done
for f in "$CK"/ledgers/CF1/scripts/CF1-c-r17/mutants/*.py "$CK"/ledgers/CF1/scripts/CF1-c-r18/mutants/*.py; do
  b=$(basename "$f" .py)
  case "$b" in *L06*) L=L06;; *) L=L05;; esac
  "$P" -I -W error "$f" > "$OUT/$b.out" 2> "$OUT/$b.err"; rc=$?
  same=$(cmp -s "$OUT/$b.out" "$OUT/base_$L.out" && echo same-output || echo DIFFERENT-output)
  echo "$b rc=$rc $same"
done
