#!/bin/sh
# Round-1 delta verifier (M3 slice d): stage the M3 grader in scratch; collect-only, reference and starter runs (QF_SEED=0).
ROOT="$(pwd)"
OUT="$ROOT/ledgers/M3/scripts/M3-d-r1/out"
WS=/private/tmp/verifyD1-M3-d-ws
PY="$ROOT/.venv/bin/python"
G="$ROOT/course/modules/M/M3/grader"
rm -rf "$WS"; mkdir -p "$WS/ref" "$WS/starter"
cp "$G/instance.py" "$G/test_project.py" "$WS/ref/"
cp "$G/reference.py" "$WS/ref/covariance_doctor.py"
cp "$G/instance.py" "$G/test_project.py" "$WS/starter/"
cp "$G/starter.py" "$WS/starter/covariance_doctor.py"
(cd "$WS/ref" && "$PY" -m pytest --collect-only -q -p no:cacheprovider test_project.py > "$OUT/collect_only_M3.out" 2>&1; echo "EXIT $?" >> "$OUT/collect_only_M3.out")
(cd "$WS/ref" && QF_SEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$OUT/reference_seed0_r1.out" 2>&1; echo "EXIT $?" >> "$OUT/reference_seed0_r1.out")
(cd "$WS/starter" && QF_SEED=0 "$PY" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$OUT/starter_seed0_r1.out" 2>&1; echo "EXIT $?" >> "$OUT/starter_seed0_r1.out")
tail -3 "$OUT/collect_only_M3.out"; tail -3 "$OUT/reference_seed0_r1.out"; tail -3 "$OUT/starter_seed0_r1.out"
