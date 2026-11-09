#!/bin/sh
# Round-12 verifier (M3 slice d): run each correct alternative in ledgers/M3/alternatives/ against the M3 suite on
# seeds 0-49 under the browser flags (ruling 10). Each alternative is staged as covariance_doctor.py in scratch.
ROOT="$(pwd)"
OUT="$ROOT/ledgers/M3/scripts/M3-d-r12/out"
PY="$ROOT/.venv/bin/python"
G="$ROOT/course/modules/M/M3/grader"
BASE=/private/tmp/verifyD12-M3-alts
rm -rf "$BASE"; mkdir -p "$BASE"
one() {
  alt="$1"; name=$(basename "$alt" .py); d="$BASE/$name"; mkdir -p "$d"
  cp "$G/instance.py" "$G/test_project.py" "$d/"; cp "$alt" "$d/covariance_doctor.py"
  fails=""
  for s in $(seq 0 49); do
    if ! (cd "$d" && QF_SEED=$s "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$d/seed$s.out" 2>&1); then
      fails="$fails $s"
    fi
  done
  if [ -z "$fails" ]; then echo "$name: PASS seeds 0-49"; else echo "$name: FAIL seeds:$fails"; fi
}
export -f one 2>/dev/null
for alt in "$ROOT"/ledgers/M3/alternatives/*.py; do one "$alt" & done
wait
