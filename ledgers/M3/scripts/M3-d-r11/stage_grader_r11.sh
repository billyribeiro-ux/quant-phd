#!/bin/sh
# Round-11 verifier (M3 slice d): stage the M3 grader in scratch and record collect-only, reference and starter runs
# under the browser flags (QF_SEED=0). Run from the checkout root: sh ledgers/M3/scripts/M3-d-r11/stage_grader_r10.sh
set -e
ROOT="$(pwd)"
OUT="$ROOT/ledgers/M3/scripts/M3-d-r11/out"
WS=/private/tmp/verifyD11-M3-d-ws-r10
PY="$ROOT/.venv/bin/python"
G="$ROOT/course/modules/M/M3/grader"
rm -rf "$WS"; mkdir -p "$WS/ref" "$WS/starter"
cp "$G/instance.py" "$G/test_project.py" "$WS/ref/"
cp "$G/reference.py" "$WS/ref/covariance_doctor.py"
cp "$G/instance.py" "$G/test_project.py" "$WS/starter/"
cp "$G/starter.py" "$WS/starter/covariance_doctor.py"
(cd "$WS/ref" && "$PY" -m pytest --collect-only -q -p no:cacheprovider test_project.py > "$OUT/collect_only_M3.out" 2>&1 || true)
(cd "$WS/ref" && QF_SEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$OUT/reference_seed0_r11.out" 2>&1 || true)
(cd "$WS/starter" && QF_SEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$OUT/starter_seed0_r11.out" 2>&1 || true)
tail -1 "$OUT/collect_only_M3.out"; tail -1 "$OUT/reference_seed0_r11.out"; tail -1 "$OUT/starter_seed0_r11.out"
