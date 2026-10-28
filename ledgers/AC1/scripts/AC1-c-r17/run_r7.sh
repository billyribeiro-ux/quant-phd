#!/bin/sh
# Seed sweep (10 seeds) for both lab twins and three student-error mutants, run from the checkout.
# Usage: sh ledgers/AC1/scripts/AC1-c-r7/seed_sweep_and_mutants.sh /tmp/AC1-v/AC1-c-r17/c7
CHK=/tmp/verify17-AC1-c
S=${1:-/tmp/AC1-v/AC1-c-r17/c7}
PY=$CHK/.venv/bin/python
mkdir -p "$S/sweep"
for L in L07 L08; do
  for s in 0 1 2 3 7 42 999 123456789 20260701 20260702; do
    sed -E "s/^SEED = [0-9_]+/SEED = $s/" $CHK/tests/labs/AC1/lab-AC1-$L-1.py > "$S/sweep/$L-$s.py"
    out=$($PY -I -W error "$S/sweep/$L-$s.py" 2>&1); rc=$?
    echo "$L seed $s rc=$rc $(echo "$out" | grep -E '^(schedule|CFO|cash|assets|APIC|deferred expense|tax expense|pretax income)' | sed -E 's/.*: //' | tr '\n' ' ')"
  done
done
sed 's/        deferred = dtl - previous_dtl/        deferred = RATE_PERCENT * taxable \/\/ 100/' $CHK/tests/labs/AC1/lab-AC1-L08-1.py > "$S/m8a.py"
sed 's/    if index == grant.vest_years - 1:/    if False:/' $CHK/tests/labs/AC1/lab-AC1-L07-1.py > "$S/m7a.py"
sed 's/    return base$/    return base + 1/' $CHK/tests/labs/AC1/lab-AC1-L07-1.py > "$S/m7b.py"
for f in m8a m7a m7b; do $PY -I -W error "$S/$f.py" >/dev/null 2>&1; echo "$f rc=$? (nonzero means the assertion killed the mutant)"; done
