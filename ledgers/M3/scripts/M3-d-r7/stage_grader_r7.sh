#!/bin/sh
# Round-7 verifier (slice d): stage the M3 grader in scratch directories and record collect-only, the reference run and the
# starter run, with the browser's flags. Run from the checkout root: sh ledgers/M3/scripts/M3-d-r7/stage_grader_r7.sh
set -e
ROOT="$(pwd)"
OUT="$ROOT/ledgers/M3/scripts/M3-d-r7/out"
WS=/private/tmp/verifyD7-M3-d-ws-r7
PY="$ROOT/.venv/bin/python"
G="$ROOT/course/modules/M/M3/grader"
rm -rf "$WS"; mkdir -p "$WS/ref" "$WS/starter"
cp "$G/instance.py" "$G/test_project.py" "$WS/ref/"
cp "$G/reference.py" "$WS/ref/covariance_doctor.py"
cp "$G/instance.py" "$G/test_project.py" "$WS/starter/"
cp "$G/starter.py" "$WS/starter/covariance_doctor.py"
(cd "$WS/ref" && "$PY" -m pytest --collect-only -q -p no:cacheprovider test_project.py > "$OUT/collect_only_M3.out" 2>&1 || true)
(cd "$WS/ref" && QF_SEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$OUT/reference_seed0_r7.out" 2>&1 || true)
(cd "$WS/starter" && QF_SEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$OUT/starter_seed0_r7.out" 2>&1 || true)
tail -1 "$OUT/collect_only_M3.out"; tail -1 "$OUT/reference_seed0_r7.out"; tail -1 "$OUT/starter_seed0_r7.out"
