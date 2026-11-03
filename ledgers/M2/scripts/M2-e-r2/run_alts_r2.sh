#!/bin/sh
# Round-2 verifier: runs the M2 grader suite (copied unchanged from grader/) against each of the five alternative
# engines in alts/ over seeds 0-49. Usage: sh run_alts_r2.sh <checkout>   Scratch copies go to /tmp/m2e_r2/alts.
CK="$1"
S=ledgers/M2/scripts/M2-e-r2
G="$CK/course/modules/M/M2/grader"
PY="$CK/.venv/bin/python"
W=/tmp/m2e_r2/alts
for pair in alt1:alt1_richardson_central alt2:alt2_complex_step_ad alt3:alt3_reverse_mode_ad alt4:alt4_recursive_sensitivities alt5:alt5_numpy_vectorized; do
  a=${pair%%:*}; f=${pair#*:}
  mkdir -p "$W/$a" && cp "$G/instance.py" "$G/test_project.py" "$W/$a/" && cp "$CK/$S/alts/$f.py" "$W/$a/sensitivity_engine.py"
  pass=0; fail=0
  for s in $(seq 0 49); do
    if (cd "$W/$a" && QF_SEED=$s "$PY" -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py >/dev/null 2>&1); then pass=$((pass+1)); else fail=$((fail+1)); echo "  $a seed $s FAILED"; fi
  done
  echo "$a ($f): $pass/50 seeds pass, $fail failing"
done
