# M7 equivalent mutants (ruling 9)

These nine files are mutants of the M7 reference solver (`course/modules/M/M7/grader/reference.py`) that differ from it
only in what they report. Under ruling 9 and VERIFIER_RULES 2.6(3) they are kept here, outside `ledgers/M7/mutants/`,
with their proofs. The graders and the page are unchanged.

Round 16 regenerated all nine files from the round-16 reference (the reference's start handling changed, see
"Corrections"). Each file is the round-16 reference with one planted change and a docstring whose first line names the
student error. Proofs 7 and 8 were re-proved against the round-16 reference; they are exact, so these two mutants
cannot be killed by any input and are not moved to `ledgers/M7/mutants/`.

| File | Row | Source | Student error (first docstring line) |
|---|---|---|---|
| `q04_dual_residual_without_zero_floor.py` | PRJ-D1-37 | round-14 copy, regenerated in round 16 | dual residual is the negative of the smallest multiplier, no floor at zero |
| `v11_01_dual_residual_sign_flipped_in_certificate.py` | PRJ-D1-37 | round-14 copy, regenerated in round 16 | dual residual is max(0, smallest multiplier), sign flipped |
| `v10_01_dual_residual_ignores_sector_and_turnover_multipliers.py` | PRJ-D1-37 | round-14 copy, regenerated in round 16 | dual residual checks only the box multipliers |
| `v10_02_complementary_slackness_signed_not_absolute.py` | PRJ-D1-37 | round-14 copy, regenerated in round 16 | complementary slackness is the largest signed product, absolute value left out |
| `r02_turnover_total_residual_dropped_from_primal.py` | PRJ-D1-37 | round-14 copy, regenerated in round 16 | turnover limit left out of the primal residual |
| `r04_budget_left_out_of_primal_residual.py` | PRJ-D1-37 | round-14 copy, regenerated in round 16 | budget violation left out of the primal residual |
| `r05_turnover_total_slackness_term_zeroed.py` | PRJ-D1-37 | round-14 copy, regenerated in round 16 | turnover-total slackness term uses a constraint value of zero |
| `s12_03_turnover_total_multiplier_clipped_at_zero.py` | PRJ-D1-37 | round-14 copy, regenerated in round 16 | turnover-total multiplier reported as max(0, kappa) |
| `v12_01_dual_residual_reported_without_the_floor_at_zero.py` | PRJ-R12-06 | moved from `ledgers/M7/scripts/M7-d-r12/alts_v12/equivalent_candidates/`, regenerated in round 16 | dual residual reported without the floor at zero |

Note on duplicates: `q04_...` and `v12_01_...` have identical code (only the docstring differs; both have
`dual = -min(mult_ineq)` at reference.py:315). They are kept as two files because two rows recorded them. Both are
proved below by the same argument.

Scope of the proofs: a mutant is listed here only if the argument below covers every input the page allows, or the
difference it can produce is inside the 1e-9 agreement tolerance the page states (project.html:321, ruling 25).

## Shared facts used by the proofs (locators in the round-16 reference.py)

- **F1 (working set is independent).** A row enters the working set only if it is independent of the budget row and
  the rows already in the set: reference.py:232-233 (initial set, admitted only when the slack is exactly 0) and
  reference.py:250-259 (blocking rows, with the refusal at line 258). The budget row is in every KKT system
  (reference.py:236). So the working set holds at most n-1 inequality rows, because n linearly independent rows fit in
  R^n.
- **F2 (multipliers are non-negative and some are zero).** The loop returns only when every working multiplier is
  non-negative; a negative one is removed (reference.py:237-242). Multipliers are assigned to working rows only
  (reference.py:259 and 267-270), and rows outside the working set default to 0 (reference.py:267-269 for lower, upper
  and sector). Turnover entries are `plus = (kappa + net)/2` and `minus = (kappa - net)/2` with
  `kappa = sum of the sign-form multipliers` and `|net| <= kappa` (reference.py:271-277), so they are non-negative and
  `kappa >= 0`. The working set holds at most n-1 inequality rows, so at least one of the n lower bounds and at least
  n+1 of the 2n box multipliers are zero. Hence the smallest entry of the six inequality groups is exactly 0 on every
  reference output. F2 does not depend on TOL.
- **F3 (the start is snapped, then checked exactly).** The start is checked to the starting tolerance TOL = 1e-9
  (reference.py:23, 87, 104 and the sector and bound checks in `_parse`). The search then starts from `_snapped_start`
  (reference.py:197-220, called at line 229): a weight outside its bounds is set onto the bound (line 208), a sector
  above its cap gives up the excess in proportion to its room above the lower bounds (sectors with no room are left
  alone), and the snapped start is used only if `sum|x - w0| <= tau` (line 219-220); otherwise the start is w0 itself.
  The consequences used below: (a) the budget gap is `sum(x0) - 1`, which can differ from `sum(w0) - 1` by the size of
  the snap; every KKT step keeps the budget row exact, so the output carries that gap. Measured maximum on the round-16
  sweep: 1.000e-09. (b) A row whose slack is zero at the start is admitted; a row entered by blocking has slack exactly
  0 at entry (reference.py:250-259). The only rows that can be in the working set with a negative slack are rows that
  the start violates and that the snap could not repair (the infeasible-within-tolerance fallback, or the turnover guard
  at line 220). These are the only cases where a complementary product can be non-zero; they are outside the proofs
  below, which do not use them.
- **F4 (turnover rows never go negative).** The sign-form row for a sign vector s has slack `tau - s.(x - w0)`
  (reference.py:193 gives the right-hand side `tau + s.w0`). At x = w0 the slack is tau, which is non-negative. If the
  snapped start is taken, `sum|x0 - w0| <= tau` by line 219-220, so the slack is at least `tau - |x0 - w0|_1 >= 0`.
  A step never passes a non-working row (ratio at line 251 is at most the slack), and a working row's slack is constant
  because every KKT step has `a.p = 0` for working rows. So every sign-form slack is non-negative on every output, and
  `sum_i |d_i| <= tau` on every output (take s = sign(d)).
- **F5 (active sign rows are tight in the l1 sense).** Let s be a sign vector whose row is in the working set on an
  output with `eta_s > 0`. Its slack is exactly 0 (F3b for admitted rows, and the blocking argument for rows entered
  by blocking; the rows that could be negative are not sign-form rows, by F4). So `s.d = tau`. Since `s.d <= sum|d_i| <= tau`
  (F4), equality holds throughout: `sum|d_i| = tau` and `s_i d_i = |d_i|` for every i.

The generator (`course/modules/M/M7/grader/instance.py`) produces starts whose weights are integers over 100 that sum to
exactly 100, and turnover limits from 0.05 to 0.40. On generator cases the snap never moves a start (the start is
inside every bound and cap), so every statement below is exact there too.

## Proofs

1. **q04 and v12_01 (dual residual without the floor).** The reference reports `max(0, -min m)` (reference.py:315); the
   mutant reports `-min m`. By F2 the minimum is 0 on every output, so both are 0. This holds for every input the page
   allows: the mutant is the same solver with a different report line.
2. **v11_01 (dual residual sign flipped).** The mutant reports `max(0, min m)`. By F2 `min m = 0`, so both are 0. Exact
   on every input.
3. **v10_01 (dual check over box multipliers only).** The mutant takes the minimum over the box multipliers. Those
   contain a zero (F2), so their minimum is 0; the reference's minimum over all groups is 0 too. Both dual residuals
   are 0. Exact on every input.
4. **s12_03 (turnover-total multiplier clipped at zero).** The mutant reports `max(0, kappa)`. By F2 `kappa >= 0`, so
   `max(0, kappa) = kappa`. Exact on every input.
5. **r02 (turnover gap left out of the primal residual).** The reference's gap term is `sum|d_i| - tau`
   (reference.py:305, inside the primal maximum at reference.py:306). By F4 it is `<= 0`, so it never sets the maximum
   over the 0 that the primal residual contains. Exact on every input.
6. **r04 (budget gap left out of the primal residual).** The reference's budget term is `|sum(w) - 1|`, and
   `sum(w) = sum(x0)` (F3a), which equals `sum(w0)` on generator cases (starts sum to exactly one). On starts accepted
   within TOL, and on starts the snap moves, the budget term is the size of the snap. The bound is measured, not
   analytic: the largest difference between r04 and the reference over the round-16 comparison (377 answered cases) is
   1.000e-09, which equals the page's own agreement tolerance (project.html:321). This is a measured bound, not an
   exact proof (ruling 25).
7. **r05 (turnover-total slackness term zeroed).** The reference's term is `kappa * (sum|d_i| - tau)`, the entry
   `sum(t) - tau` inside the complementary-slackness maximum (reference.py:326, with the multiplier `kappa` at line
   319). Let `kappa > 0`. Then some sign-form row has `eta_s > 0` on the output (kappa is the sum of the sign-form
   multipliers, and every multiplier is non-negative by F2). By F5, `sum|d_i| = tau`, so the term
   `sum(t) - tau` is exactly 0, and the product is 0. If `kappa = 0` the product is 0 for the same reason. The
   reference's term therefore equals 0 on every output, and the mutant, which replaces it with the constant 0, reports
   the same certificate. Exact on every input the page allows, because the argument uses only F2, F4 and F5, and those
   hold for every start the reference accepts.
8. **v10_02 (complementary slackness signed, not absolute).** The reference takes `max_k |p_k|` over the products
   `p_k = m_k g_k` (reference.py:316-326), and the mutant takes `max_k p_k` over the same list. They are equal when every
   `p_k >= 0`. Each product is non-negative on every output:
   - Box and sector pairs. Each certificate gap is minus the slack of its row: `lower_i - w_i` is minus the slack of the
     lower row, `w_i - upper_i` of the upper row, and `sum_k - cap_k` of the sector row. A row outside the working set has
     multiplier 0 (F2). A row inside the working set has slack 0 or negative (F3b), so its gap is 0 or positive. With a
     non-negative multiplier, each product is `>= 0`.
   - Turnover plus and minus pairs. `g_plus_i = d_i - t_i` is 0 when `d_i >= 0` and `2 d_i < 0` when `d_i < 0`; similarly
     `g_minus_i = -d_i - t_i` is 0 when `d_i <= 0`. Take `d_i < 0`. Then `plus_i = sum of eta_s over sign vectors with
     s_i = +1`. Such a row with `eta_s > 0` is in the working set, so by F5 `s_i d_i = |d_i|`, which for `d_i < 0` forces
     `s_i = -1`. So `plus_i = 0` and the product is 0. The case `d_i > 0` is symmetric for `minus_i`.
   - Total pair. `kappa * (sum|d_i| - tau)` is 0 by proof 7.
   So every product is `>= 0`, `max|p_k| = max p_k`, and the two reports coincide on every output. Exact on every input.

## Corrections to the earlier ledger records

- Round 15 (`PRJ-R15-02`): the round-15 verifier found that proofs 7 and 8 were measured, not proved, and that the two
  mutants were distinguishable on starts inside the tolerance (case A, tau = 1e-9, mu = [1000, 0]: reference complementary
  0 against recomputed 5e-7). That defect came from the round-15 reference admitting rows with positive slack of up to
  1e-9 into the initial working set (`PRJ-R15-01`), and the round-16 reference no longer does so. With the fixed
  reference, the two proofs above are exact, and the earlier figures (9 and 23 of 400 distinguished cases, and the
  measured maxima 7.969e-11 and 6e-7/8e-7) belong to the old reference and are superseded.
- Round 14 (`ledgers/M7/mutant_equivalence_r14.json`) stated that the reference's budget gap for r04 and its
  complementary-slackness residual for v10_02 are "exactly zero on every reference output", and that r05's turnover-total
  gap is exactly zero. Those statements hold on the generator's cases; on hand-built inputs within the starting tolerance
  they did not hold for the round-14 reference. The round-16 proofs above replace them. The JSON was not edited.
- Round 16 regenerated the nine files from the round-16 reference. Each file differs from the reference only in its
  planted change and its docstring. The earlier copies were the pre-round-16 reference (git HEAD) with the planted
  change; that reference had the start-admission defect of PRJ-R15-01.

## Evidence

- `ledgers/M7/scripts/M7-d-r16/equiv_recheck_r16.py` (run from the repository root with `.venv/bin/python -I`). It compares
  each file with the round-16 reference on the generator's cases for seeds 0-49 and on a seeded sweep of 400 random
  page-valid cases (327 of the random cases answered; 377 answered in total with the 50 generator cases), including
  starts inside the 1e-9 tolerance. Output in `ledgers/M7/scripts/M7-d-r16/equiv_recheck_r16.log`:
  - each of the nine files differs from the reference on 0 of the 377 answered cases by more than 1e-9;
  - the largest difference is 1.000e-09 for r04 and 0 for the other eight.
- `ledgers/M7/scripts/M7-d-r16/probe_fix_r16.py` and `compare_old_new_r16.py` cover the start-snap change itself (the
  hand cases and the case-by-case comparison with the committed reference).
