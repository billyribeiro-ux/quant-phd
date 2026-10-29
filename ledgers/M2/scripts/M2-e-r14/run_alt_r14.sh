#!/bin/sh
# Run one alternative engine against the M2 project suite on seeds 0-49 (same flags as tools/run_graders.py).
ROOT=/Users/billyribeiro/.fanout/wt/verifyB14-M2-e
ALT="$1"
W=$(mktemp -d /tmp/m2e_r14/alt.XXXX)
cp "$ROOT/course/modules/M/M2/grader/test_project.py" "$ROOT/course/modules/M/M2/grader/instance.py" "$W/"
cp "$ALT" "$W/sensitivity_engine.py"
cd "$W" || exit 1
pass=0; fail=0; first=""
for s in $(seq 0 49); do
  if QF_SEED=$s PYTHONHASHSEED=0 "$ROOT/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py > "$W/seed$s.log" 2>&1; then pass=$((pass+1)); else fail=$((fail+1)); [ -z "$first" ] && first="seed $s: $(grep -m1 '^FAILED' "$W/seed$s.log" | cut -c1-200)"; fi
done
echo "$(basename "$ALT"): $pass/50 seeds pass, $fail fail (work dir $W) first-fail: $first"
