#!/bin/bash
# Round 8 (SC1-d): the round-7 alternatives not yet swept in round 8 (alt3, alt5-alt9). alt1 and alt2 were swept
# in the first run; alt2b (brute-force walk enumeration) is excluded here because it stalls at n = 41 (see
# SC1-d-ag-walk-listing-stall); alt4 (Box-Muller, not the gauss draw the page states) is excluded per ruling 10.
set -u
ROOT=/Users/billyribeiro/.fanout/wt/verifyE8-SC1-d
G=$ROOT/course/modules/SC/SC1/grader
PY=$ROOT/.venv/bin/python
for name in alt3_srw_dp alt5_cumsum_index_subsample alt6_pascal_row_terminal alt7_gauss_step_major alt8_one_minus_erf alt9_se_closed_form; do
  alt="$ROOT/ledgers/SC1/scripts/SC1-d-r7/alternatives/$name.py"
  W=$(mktemp -d /tmp/sc1d-r8-alt7-XXXX)
  cp "$G/test_project.py" "$G/instance.py" "$W"/
  cp "$alt" "$W/bm_checks.py"
  pass=0; fail=""
  for s in $(seq 0 49); do
    out=$(cd "$W" && QF_SEED=$s $PY -I -m pytest -q -p no:cacheprovider --assert=plain -W error test_project.py 2>&1 | tail -1)
    if echo "$out" | grep -qx "132 passed in.*"; then pass=$((pass+1)); else fail="$fail $s"; fi
  done
  echo "$name: pass $pass/50 seeds; failing seeds:${fail:- none}"
  rm -rf "$W"
done
