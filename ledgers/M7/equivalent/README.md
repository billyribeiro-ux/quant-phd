# M7 equivalent mutants (ruling 9)

These nine files are mutants of the M7 reference solver (`course/modules/M/M7/grader/reference.py`) that differ from it
only in what they report, and only where no output of the reference solver can show a difference. Under ruling 9 and
VERIFIER_RULES 2.6(3) they are kept here, outside `ledgers/M7/mutants/`, with their proofs. The graders and the page
are unchanged.

Each file's first docstring line names the student error it models.

| File | Row | Source | Student error (first docstring line) |
|---|---|---|---|
| `q04_dual_residual_without_zero_floor.py` | PRJ-D1-37 | `git show 5e18d08d:ledgers/M7/mutants/q04_dual_residual_without_zero_floor.py` (removed in d2b4a874) | dual residual is the negative of the smallest multiplier, no floor at zero |
| `v11_01_dual_residual_sign_flipped_in_certificate.py` | PRJ-D1-37 | `git show 5e18d08d:...` | dual residual is max(0, smallest multiplier), sign flipped |
| `v10_01_dual_residual_ignores_sector_and_turnover_multipliers.py` | PRJ-D1-37 | `git show 5e18d08d:...` | dual residual checks only the box multipliers |
| `v10_02_complementary_slackness_signed_not_absolute.py` | PRJ-D1-37 | `git show 5e18d08d:...` | complementary slackness is the largest signed product, absolute value left out |
| `r02_turnover_total_residual_dropped_from_primal.py` | PRJ-D1-37 | `git show 5e18d08d:...` | turnover limit left out of the primal residual |
| `r04_budget_left_out_of_primal_residual.py` | PRJ-D1-37 | `git show 5e18d08d:...` | budget violation left out of the primal residual |
| `r05_turnover_total_slackness_term_zeroed.py` | PRJ-D1-37 | `git show 5e18d08d:...` | turnover-total slackness term uses a constraint value of zero |
| `s12_03_turnover_total_multiplier_clipped_at_zero.py` | PRJ-D1-37 | `git show 5e18d08d:...` | turnover-total multiplier reported as max(0, kappa) |
| `v12_01_dual_residual_reported_without_the_floor_at_zero.py` | PRJ-R12-06 | moved from `ledgers/M7/scripts/M7-d-r12/alts_v12/equivalent_candidates/` | dual residual reported without the floor at zero |

Note on duplicates: `q04_...` and `v12_01_...` have identical code (only the docstring differs; both have
`dual = -min(mult_ineq)` at line 289). They are kept as two files because two rows recorded them. Both are
proved below by the same argument.

Scope of the proofs: a mutant is listed here only if the argument below covers every input the page allows, or the
difference it can produce is inside a tolerance the page states (ruling 25). The witness is
`ledgers/M7/scripts/M7-d-r14/equiv.py` (run from the repository root with `.venv/bin/python -I`). Its output is in
`ledgers/M7/scripts/M7-d-r14/equiv_r14_rerun.log`.

## Shared facts used by the proofs (locators in reference.py)

- **F1 (working set is independent).** A row enters the working set only if it is independent of the budget row and
  the rows already in the set: reference.py:204 (initial set, with the test `b - a.x <= TOL`) and reference.py:229-231
  (blocking rows, with the refusal at line 230). The budget row is in every KKT system (reference.py:208). So the
  working set holds at most n-1 inequality rows, because n linearly independent rows fit in R^n.
- **F2 (multipliers are non-negative and some are zero).** The loop returns only when every working multiplier is
  non-negative; a negative one is removed (reference.py:210-214). Multipliers are assigned to working rows only
  (reference.py:212), and rows outside the working set default to 0 (reference.py:239-241 for lower, upper and sector).
  Turnover entries are `plus = (kappa + net)/2` and `minus = (kappa - net)/2` with `kappa = sum of the sign-form
  multipliers` and `|net| <= kappa` (reference.py:243-249), so they are non-negative and `kappa >= 0`. The working set
  holds at most n-1 inequality rows, so at least one of the n lower bounds and at least n+1 of the 2n box multipliers are
  zero. Hence the smallest entry of the six inequality groups is exactly 0 on every reference output. F2 does not
  depend on TOL.
- **F3 (the TOL-scale exceptions).** The reference accepts starts within the starting tolerance TOL = 1e-9
  (reference.py:21, 102-107), which is the tolerance the page states (project.html:321). Two consequences:
  (a) the budget gap is `sum(w0) - 1`, not zero in general, because every KKT step keeps the budget row exact
  (reference.py:208); its size is at most TOL; (b) a row entered at the start with slack in `[-TOL, TOL]`
  (reference.py:204; a bound row can start up to TOL outside its bound) keeps that slack, since steps are orthogonal to
  working rows, so some complementary products can be non-zero, of size slack times multiplier. Rows entered by blocking
  have slack exactly 0 (reference.py:222-231).
- **F4 (turnover rows).** Every sign-form row `sum_i s_i d_i <= tau` (reference.py:189-191) starts with slack `tau` and
  is never stepped past, so its slack stays `>= 0`. Hence `sum_i |d_i| <= tau` on every output (take s = sign(d)).

The generator (`course/modules/M/M7/grader/instance.py:24-33, 45-55`) produces starts whose weights are integers over
100 that sum to exactly 100, and turnover limits from 0.05 to 0.40. So on generator cases F3 never applies and every
statement below is exact.

## Proofs

1. **q04 and v12_01 (dual residual without the floor).** The reference reports `max(0, -min m)` (reference.py:287); the
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
   (reference.py:277, inside the primal maximum at reference.py:278). By F4 it is `<= 0`, so it never sets the maximum
   over the 0 that the primal residual contains. Exact on every input.
6. **r04 (budget gap left out of the primal residual).** The reference's budget term is `|sum(w) - 1| = |sum(w0) - 1|`
   (F3a). It is exactly 0 on every generator case (starts sum to exactly one). On starts accepted within TOL it is at
   most 1e-9, and the mutant's primal residual differs from the reference's by that amount. That is the page's own
   agreement tolerance (project.html:321), so the mutant survives every test the page justifies. This is a measured
   bound, not an exact proof (ruling 25). The measured maximum is 9.000e-10.
7. **r05 (turnover-total slackness term zeroed).** The reference's term is `kappa * (sum|d_i| - tau)`, inside the
   complementary-slackness maximum at reference.py:288-297. If `kappa > 0`, some working sign-form row has a positive
   multiplier. A sign-form row enters the initial working set only when `tau <= TOL` (reference.py:204); otherwise it
   enters by blocking with slack exactly 0 (F3b). So for `tau = 0` or `tau > 1e-9` every working sign-form row has
   slack 0. Then `sum_i s_i d_i = tau` for that row, and with F4 `tau = sum_i s_i d_i <= sum_i |d_i| <= tau`, so the gap
   is exactly 0 and the term is 0. For `0 < tau <= 1e-9` the difference is at most `kappa` times a slack of size at most
   1e-9. This is measured, not proved, for those turnover limits. The measured maximum is 7.969e-11 (turnover limits
   1e-10 and 9e-10 in the sweep).
8. **v10_02 (complementary slackness signed, not absolute).** The reference takes `max |m g|` (reference.py:288-296),
   the mutant takes the largest signed `m g`. They differ only when some product `m g` is negative and attains the
   maximum of the absolute values. By F3(b) every product is exactly 0 when each working row has slack 0, so the two
   agree on every input without a TOL-scale start. For TOL-scale starts the difference is at most the product of a
   multiplier and a slack of size at most 1e-9. This is measured, not proved. The measured maximum is 7.969e-11.

## Corrections to the round-14 ledger record

`ledgers/M7/mutant_equivalence_r14.json` states that the reference's budget gap for r04 and its complementary-slackness
residual for v10_02 are "exactly zero on every reference output", and that r05's turnover-total gap is exactly zero.
Those statements hold on the generator's cases (exact-one starts, turnover limits above TOL) but not on hand-built
inputs within the 1e-9 starting tolerance (F3). The proofs above replace those statements. The JSON was not edited.

## Evidence

- `ledgers/M7/scripts/M7-d-r14/equiv.py` (repository-relative; reads `ledgers/M7/equivalent/*.py`; seeds 0-299 exact,
  and a boundary sweep over seeds 0-49). Output in `ledgers/M7/scripts/M7-d-r14/equiv_r14_rerun.log`:
  - each of the nine mutants differs from the reference on 0 of 300 exact seeds;
  - the reference's smallest inequality multiplier is exactly 0 on 300 of 300 exact seeds and 450 of 450 sweep answers;
  - sweep: 450 answered, 0 refused. Largest certificate difference per mutant: r04 9.000e-10; r05 7.969e-11; v10_02
    7.969e-11; all other mutants 0.
- `ledgers/M7/scripts/M7-d-r12/alts_v12/equiv_v12_01.py` (repository root passed as argument) draws 400 random small
  cases on top of the 50 generator cases. Output in `ledgers/M7/scripts/M7-d-r12/alts_v12/equiv_v12_01_rerun_r14.log`:
  `cases answered: 450; refused: 0; answers with every inequality entry > 0: 0`.
- The untracked `ledgers/M7/scripts/M7-d-r14/equiv_witness_r14.py` and `equiv_removed_r14/` are an earlier copy of
  the same check. They are superseded by `equiv.py`.
