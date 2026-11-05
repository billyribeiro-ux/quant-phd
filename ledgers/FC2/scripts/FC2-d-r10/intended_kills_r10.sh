#!/bin/sh
# usage: intended_kills_r10.sh <repo_root>; runs each round-10 mutant against its intended killer test(s) on seed 0
ROOT="$1"
G="$ROOT/course/modules/FC/FC2/grader"
run() {
  name="$1"; test="$2"
  T=$(mktemp -d)
  cp "$ROOT/ledgers/FC2/mutants/$name" "$T/scanner.py"
  cp "$G/test_project.py" "$G/instance.py" "$T/"
  ( cd "$T" && QF_SEED=0 "$ROOT/.venv/bin/python" -m pytest -q -p no:cacheprovider --assert=plain -W error "test_project.py" -k "$test" >/dev/null 2>&1; echo "$name [$test] pytest rc=$?" )
  rm -rf "$T"
}
run z10_a_strike_of_one_cent_rejected.py test_parity_gap_rejects_a_nonpositive_strike_and_accepts_one
run z10_b_df_upper_bound_exclusive.py test_parity_gap_df_range_upper_boundary
run z10_c_zero_half_spread_rejected.py test_negative_half_spread_is_rejected_and_zero_is_accepted
run z10_d_convexity_flags_call_below_chord.py test_clean_calls_give_no_convexity_violation
