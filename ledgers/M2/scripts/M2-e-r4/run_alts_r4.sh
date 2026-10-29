#!/bin/sh
# Round 4: copies the current grader (instance.py, test_project.py) next to each alternative and runs seeds 0-49.
CK=/tmp/verifyB4-M2-e
G="$CK/course/modules/M/M2/grader"
W=/tmp/M2-v/M2-e-r4/alts
for src in "$CK/ledgers/M2/scripts/M2-e-r2/alts/alt1" "$CK/ledgers/M2/scripts/M2-e-r2/alts/alt2" "$CK/ledgers/M2/scripts/M2-e-r2/alts/alt3" "$CK/ledgers/M2/scripts/M2-e-r2/alts/alt4" "$CK/ledgers/M2/scripts/M2-e-r2/alts/alt5" "$CK/ledgers/M2/scripts/M2-e-r3/alts/alt1" "$CK/ledgers/M2/scripts/M2-e-r3/alts/alt2" "$CK/ledgers/M2/scripts/M2-e-r3/alts/alt3" "$CK/ledgers/M2/scripts/M2-e-r4/alts/alt4" "$CK/ledgers/M2/scripts/M2-e-r4/alts/alt5" "$CK/ledgers/M2/scripts/M2-e-r4/alts/alt6"; do
  [ -d "$src" ] || continue
  a=$(echo "$src" | sed 's#.*/scripts/##; s#/#_#g')
  mkdir -p "$W/$a" && cp "$G/instance.py" "$G/test_project.py" "$W/$a/" && cp "$src/sensitivity_engine.py" "$W/$a/"
  echo "== $a"
  (cd "$W/$a" && for s in $(seq 0 49); do QF_SEED=$s "$CK/.venv/bin/python" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1; done | sed 's/ in .*//' | sort | uniq -c)
done
