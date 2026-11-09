#!/bin/sh
# Round-15: each file in ledgers/M7/equivalent matches git 5e18d08d:ledgers/M7/mutants/<name> (removed in d2b4a874); run from the repository root.
for f in q04_dual_residual_without_zero_floor r02_turnover_total_residual_dropped_from_primal r04_budget_left_out_of_primal_residual r05_turnover_total_slackness_term_zeroed s12_03_turnover_total_multiplier_clipped_at_zero v10_01_dual_residual_ignores_sector_and_turnover_multipliers v10_02_complementary_slackness_signed_not_absolute v11_01_dual_residual_sign_flipped_in_certificate; do
  if git show "5e18d08d:ledgers/M7/mutants/$f.py" > /tmp/m7r15_src.py 2>/dev/null && cmp -s /tmp/m7r15_src.py "ledgers/M7/equivalent/$f.py"; then echo "SAME $f"; else echo "DIFF-OR-MISSING $f"; fi
done
git show "1431aa1d:ledgers/M7/mutants/v12_01_dual_residual_reported_without_the_floor_at_zero.py" >/dev/null 2>&1 && echo "note: v12_01 existed at 1431aa1d under mutants" || echo "v12_01 not under mutants at 1431aa1d"
ls ledgers/M7/equivalent/*.py | wc -l
