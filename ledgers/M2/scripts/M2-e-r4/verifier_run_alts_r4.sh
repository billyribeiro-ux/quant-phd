#!/bin/sh
# Round 4: current grader vs alternatives (r2 alt1-5, r3 alt1-3) over seeds 0-49. Usage: sh run_alts_r4.sh <checkout>
CK="$1"; G="$CK/course/modules/M/M2/grader"; W=/tmp/M2-v/M2-e-r4/alts
for d in r2/alt1 r2/alt2 r2/alt3 r2/alt4 r2/alt5 r3/alt1 r3/alt2 r3/alt3; do
  a=$(echo $d | tr / _); src="$CK/ledgers/M2/scripts/M2-e-$(dirname $d)/alts/$(basename $d)"
  mkdir -p "$W/$a" && cp "$G/instance.py" "$G/test_project.py" "$W/$a/" && cp "$src/sensitivity_engine.py" "$W/$a/"
  echo "== $a"
  (cd "$W/$a" && for s in $(seq 0 49); do QF_SEED=$s "$CK/.venv/bin/python" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1; done | sed 's/ in .*//' | sort | uniq -c)
done
