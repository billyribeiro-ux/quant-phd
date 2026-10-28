#!/bin/sh
# Round 8 new student-error mutants of the lab twins (one sed edit each), run under -I -W error.
CHK=/tmp/verify17-AC1-c
S=/tmp/AC1-v/AC1-c-r17/c8/m
PY=$CHK/.venv/bin/python
T7=$CHK/tests/labs/AC1/lab-AC1-L07-1.py
T8=$CHK/tests/labs/AC1/lab-AC1-L08-1.py
sed 's|    base = grant.value_cents // grant.vest_years|    base = -(-grant.value_cents // grant.vest_years)|' $T7 > $S/n1ceil.py
sed 's|    base = grant.value_cents // grant.vest_years|    base = grant.value_cents // grant.vest_years + (1 if grant.value_cents % grant.vest_years else 0)|' $T7 > $S/n1b.py
sed 's|        book_dep = cost // LIFE|        book_dep = cost // (LIFE - 1)|' $T8 > $S/n2life.py
sed 's|        deferred = dtl - previous_dtl|        deferred = previous_dtl - dtl|' $T8 > $S/n3sign.py
sed 's|        tax_expense = current + deferred|        tax_expense = current|' $T8 > $S/n4te.py
for f in n1ceil n1b n2life n3sign n4te; do
  $PY -I -W error $S/$f.py >$S/$f.out 2>$S/$f.err; echo "$f rc=$? $(tail -1 $S/$f.err)"
done
