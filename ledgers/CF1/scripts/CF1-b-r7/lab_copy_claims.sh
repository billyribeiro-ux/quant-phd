#!/bin/sh
# Round 7, CF1-b: runs modified copies of the L03 twin to check the E2 and E3 solution claims.
# Usage: sh lab_copy_claims.sh <checkout> <scratch>
set -e
CK="$1"; SCR="$2"; PY="$CK/.venv/bin/python"
mkdir -p "$SCR"
sed -e 's/^REAL_RATE = 0.06/REAL_RATE = 0.10/' "$CK/tests/labs/CF1/lab-CF1-L03-1.py" > "$SCR/e3_copy.py"
sed -e 's/^INFLATION = 0.03/INFLATION = 0.00/' "$CK/tests/labs/CF1/lab-CF1-L03-1.py" > "$SCR/e2_copy.py"
"$PY" -I -W error "$SCR/e3_copy.py" | grep -E 'nominal rate|largest absolute gap'
"$PY" -I -W error "$SCR/e2_copy.py" | grep -E 'mixed minus real, cents|NPV real flows at nominal rate'
