#!/bin/sh
# Round-11 verifier (M3 slice d): run each correct alternative in ledgers/M3/alternatives/ against the M3 suite on
# seeds 0-9, under the browser flags. Each alternative is copied as covariance_doctor.py into a scratch directory.
ROOT="$(pwd)"
OUT="$ROOT/ledgers/M3/scripts/M3-d-r11/out"
PY="$ROOT/.venv/bin/python"
G="$ROOT/course/modules/M/M3/grader"
BASE=/private/tmp/verifyD11-M3-alts-r10
rm -rf "$BASE"; mkdir -p "$BASE"
: > "$OUT/alts_seeds0-9_r11.out"
for alt in "$ROOT"/ledgers/M3/alternatives/*.py; do
  name=$(basename "$alt" .py)
  d="$BASE/$name"; mkdir -p "$d"
  cp "$G/instance.py" "$G/test_project.py" "$d/"
  cp "$alt" "$d/covariance_doctor.py"
  fails=""
  for s in 0 1 2 3 4 5 6 7 8 9; do
    if ! (cd "$d" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$d/seed$s.out" 2>&1); then
      fails="$fails $s"
    fi
  done
  if [ -z "$fails" ]; then echo "$name: PASS seeds 0-9 (163 tests each)" >> "$OUT/alts_seeds0-9_r11.out"; else echo "$name: FAIL seeds:$fails" >> "$OUT/alts_seeds0-9_r11.out"; fi
done
cat "$OUT/alts_seeds0-9_r11.out"
