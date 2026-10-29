#!/bin/sh
# Run one alternative engine against the M2 project suite on seeds 0-49 (same flags as tools/run_graders.py).
ALT="$1"
ROOT=/Users/billyribeiro/.fanout/wt/verifyB12-M2-e
W=$(mktemp -d /tmp/m2e_r12/alt.XXXX)
cp "$ROOT/course/modules/M/M2/grader/test_project.py" "$ROOT/course/modules/M/M2/grader/instance.py" "$W/"
cp "$ALT" "$W/sensitivity_engine.py"
cd "$W" || exit 1
pass=0; fail=0
for s in $(seq 0 49); do
  if QF_SEED=$s PYTHONHASHSEED=0 "$ROOT/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$W/seed$s.log" 2>&1; then pass=$((pass+1)); else fail=$((fail+1)); fi
done
echo "$(basename "$ALT"): $pass/50 seeds pass, $fail fail (work dir $W)"
