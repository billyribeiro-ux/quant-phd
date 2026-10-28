#!/bin/sh
# Round 8 re-run of the lab mutants and the ten-seed sweep, on the checkout's own twins.
CHK=/tmp/verify8-AC1-c
S=/tmp/AC1-v/c8
PY=$CHK/.venv/bin/python
sed 's/        deferred = dtl - previous_dtl/        deferred = RATE_PERCENT * taxable \/\/ 100/' $CHK/tests/labs/AC1/lab-AC1-L08-1.py > "$S/m/m8a.py"
sed 's/    if index == grant.vest_years - 1:/    if False:/' $CHK/tests/labs/AC1/lab-AC1-L07-1.py > "$S/m/m7a.py"
sed 's/    return base$/    return base + 1/' $CHK/tests/labs/AC1/lab-AC1-L07-1.py > "$S/m/m7b.py"
for f in m8a m7a m7b; do
  cmp -s "$S/m/$f.py" "$CHK/tests/labs/AC1/lab-AC1-L0${f#m}" 2>/dev/null
  $PY -I -W error "$S/m/$f.py" >"$S/m/$f.out" 2>"$S/m/$f.err"; echo "$f rc=$? last-error: $(tail -1 $S/m/$f.err)"
done
for L in L07 L08; do
  for s in 0 1 2 3 7 42 999 123456789 20260701 20260702; do
    sed -E "s/^SEED = [0-9_]+/SEED = $s/" $CHK/tests/labs/AC1/lab-AC1-$L-1.py > "$S/m/$L-$s.py"
    out=$($PY -I -W error "$S/m/$L-$s.py" 2>&1); rc=$?
    echo "$L seed $s rc=$rc checks=$(echo "$out" | grep -cE '(sum|identit|hold|equal|balance|ok|exact)')"
  done
done
