# M7 equivalent mutants (ruling 9, ruling 35)

These eighteen files are mutants of the M7 reference solver (`course/modules/M/M7/grader/reference.py`) that no input
the page's contract allows can tell apart from the reference. Under ruling 9 and VERIFIER_RULES 2.6(3) they are kept
here, outside `ledgers/M7/mutants/`, with their proofs. The graders and the page are not changed by this folder.

Ruling 35 sets the contract for a starting portfolio: it is feasible exactly when its decimal values are read exactly,
and a start that breaches the budget, a bound or a sector cap by a tolerance-level amount is outside the contract. The
reference refuses every such start with `ValueError` (reference.py:104-110) and never snaps a start (reference.py:203).
Under that contract, a mutant is equivalent when it agrees with the reference on every start the reference accepts.

| File | Row | Source | Student error (first docstring line) |
|---|---|---|---|
| `q04_dual_residual_without_zero_floor.py` | PRJ-D1-37 | regenerated in round 16 (ruling 35) | dual residual is the negative of the smallest multiplier, no floor at zero |
| `v12_01_dual_residual_reported_without_the_floor_at_zero.py` | PRJ-R12-06 | regenerated in round 16 (ruling 35) | dual residual reported without the floor at zero |
| `v11_01_dual_residual_sign_flipped_in_certificate.py` | PRJ-D1-37 | regenerated in round 16 (ruling 35) | dual residual is max(0, smallest multiplier), sign flipped |
| `v10_01_dual_residual_ignores_sector_and_turnover_multipliers.py` | PRJ-D1-37 | regenerated in round 16 (ruling 35) | dual residual checks only the box multipliers |
| `v10_02_complementary_slackness_signed_not_absolute.py` | PRJ-D1-37 | regenerated in round 16 (ruling 35) | complementary slackness is the largest signed product, absolute value left out |
| `r02_turnover_total_residual_dropped_from_primal.py` | PRJ-D1-37 | regenerated in round 16 (ruling 35) | turnover limit left out of the primal residual |
| `r04_budget_left_out_of_primal_residual.py` | PRJ-D1-37, PRJ-R14-01, PRJ-R15-04 | regenerated in round 16 (ruling 35) | budget violation left out of the primal residual |
| `r05_turnover_total_slackness_term_zeroed.py` | PRJ-D1-37 | regenerated in round 16 (ruling 35) | turnover-total slackness term uses a constraint value of zero |
| `s12_03_turnover_total_multiplier_clipped_at_zero.py` | PRJ-D1-37 | regenerated in round 16 (ruling 35) | turnover-total multiplier reported as max(0, kappa) |
| `r16_02_start_used_without_snapping.py` | PRJ-R16-01 | moved from `ledgers/M7/mutants/` (ruling 35) | the starting portfolio is used as it is |
| `r16_03_lower_start_not_snapped_up.py` | PRJ-R16-01 | moved from `ledgers/M7/mutants/` (ruling 35) | a weight below its lower bound at the start is left below it |
| `r16_04_sector_excess_taken_from_first_member.py` | PRJ-R16-01 | moved from `ledgers/M7/mutants/` (ruling 35) | a sector's excess is taken from its first member alone |
| `r16_05_sector_excess_left_in_place.py` | PRJ-R16-01 | moved from `ledgers/M7/mutants/` (ruling 35) | a sector breaching its cap by up to the tolerance is not moved back |
| `r16_06_snap_taken_beyond_the_turnover_limit.py` | PRJ-R16-01 | moved from `ledgers/M7/mutants/` (ruling 35) | the snapped start is used even when it moves beyond the turnover limit |
| `v16d_01_snap_ignores_sector_caps.py` | PRJ-R16-01 | moved from `ledgers/M7/mutants/` (ruling 35) | the starting sector caps are not repaired before the search |
| `v16d_02_turnover_guard_dropped_from_snap.py` | PRJ-R16-01 | moved from `ledgers/M7/mutants/` (ruling 35) | the snapped start is used beyond the turnover limit |
| `v16d_03_sector_excess_all_from_first_member.py` | PRJ-R16-01 | moved from `ledgers/M7/mutants/` (ruling 35) | a sector's excess is taken from its first member without checking its room |
| `s05_start_sum_tolerance_1e-10.py` | PRJ-R16-01 | round-4 mutant, regenerated in round 16 as a single change | the starting-portfolio tolerance is 1e-10 |

Note on duplicates: `q04_...` and `v12_01_...` have identical code (only the docstring differs; both have
`dual = -min(mult_ineq)` at reference.py:289). They are kept as two files because two rows recorded them.

Note on the nine moved files: before ruling 35 each was killed by a test of a tolerance-level start. Eight were killed
by the hand cases that ruling 35 removes (the start breaching a bound or a cap by one billionth), and s05 by the removed
accept test of a sum 5e-10 off one. They are full modules derived from the round-16 reference before ruling 35, which
contained the snapping function. Their proofs below use only the behaviour they share with the current reference on
exact starts.

## Shared facts (locators in the current reference.py)

- **F0 (exact start).** `_parse` checks the budget, the bounds and the sector caps exactly (reference.py:104-110), so
  `sum(w0) = 1` exactly, `lower <= w0 <= upper` and `sum over S_k of w0 <= c_k` on every case the reference accepts. The
  search starts at `x = w0` (reference.py:203). The budget row is an equality in every KKT system
  (reference.py:210, `[budget] + working`), and `_kkt_step` solves `A p = 0` for those rows (reference.py:164-178). So
  `budget . p = 0` exactly, and `sum(x) = 1` at every iterate, in Fraction arithmetic. The output `w` equals the last
  iterate `x`.
- **F1 (working set is independent and holds at most n-1 inequality rows).** A row enters the working set only if it is
  independent of the budget row and the rows already in the set: the initial admission at reference.py:206 (admitted
  only when the slack is exactly 0) and the blocking admission at reference.py:229-233 (with the refusal at line 232).
  Because the budget row is always present, at most n-1 inequality rows are active at any iterate.
- **F2 (multipliers are non-negative, and some are zero).** The loop returns only when every working multiplier is
  non-negative; a negative one is removed (reference.py:211-216). Multipliers are assigned to working rows only, and rows
  outside the working set default to 0 (reference.py:241-243 for lower, upper and sector). Turnover entries are
  `plus = (kappa + net)/2` and `minus = (kappa - net)/2` with `kappa = sum of the sign-form multipliers` and
  `|net| <= kappa` (reference.py:244-251), so both are non-negative and `kappa >= 0`. By F1, at most n-1 of the 2n box
  rows are active, so at least one lower multiplier is 0 and at least n+1 of the 2n box multipliers are 0. Hence the
  smallest inequality multiplier is exactly 0 on every reference output.
- **F3 (every row keeps a non-negative slack, exactly).** At `x = w0` every slack is non-negative by F0, and every sign-form
  slack is `tau - s.(w0 - w0) = tau >= 0`. A step moves `x` by `step * p` with `step` at most each non-working row's ratio
  (reference.py:218-227), so no non-working slack becomes negative, and a working row has `a.p = 0` (F0) so its slack
  stays where it is. A blocking row's slack becomes exactly 0 at entry, because `step` equals its ratio. So every slack
  is non-negative on every iterate, every working slack is exactly 0, and the primal residual's box, cap and turnover
  terms are at most 0 on every output.
- **F4 (turnover).** Every sign-form slack is non-negative (F3), so `s.(w - w0) <= tau` for all `2^n` sign vectors `s`.
  Taking `s = sign(d)` (with `sign(0) = +1`) gives `sum_i |d_i| <= tau` on every output.
- **F5 (active sign rows are tight in the l1 sense).** Let `s` be a sign vector whose row is in the working set on an
  output with `eta_s > 0`. Its slack is exactly 0 (F1, F3), so `s.d = tau`. By F4, `s.d <= sum|d_i| <= tau`, so equality
  holds throughout: `sum|d_i| = tau` and `s_i d_i = |d_i|` for every i.

## Proofs

1. **q04 and v12_01 (dual residual without the floor).** The reference reports `max(0, -min m)` (reference.py:289); the
   mutant reports `-min m`. By F2 the minimum over all inequality multipliers is 0, so both reports are 0. Exact on
   every input the reference accepts.
2. **v11_01 (dual residual sign flipped).** The mutant reports `max(0, min m)`. By F2 `min m = 0`, so both are 0.
3. **v10_01 (dual check over box multipliers only).** The mutant takes the minimum over the box multipliers. They contain
   a zero (F2), so their minimum is 0, and the reference's minimum over all groups is 0 too. Both are 0.
4. **s12_03 (turnover-total multiplier clipped at zero).** The mutant reports `max(0, kappa)`. By F2 `kappa >= 0`, so
   `max(0, kappa) = kappa`.
5. **r02 (turnover gap left out of the primal residual).** The reference's gap term is `sum|d_i| - tau`
   (reference.py:279, inside the primal maximum at line 280). By F4 it is `<= 0`, so it never sets the maximum over the 0
   that the primal residual contains.
6. **r04 (budget gap left out of the primal residual).** The reference's budget term is `|sum(w) - 1|` (reference.py:280).
   By F0 it is exactly 0 on every output the reference accepts: the start sums to one exactly, and every step keeps the
   sum exactly. So the mutant's primal residual equals the reference's on every accepted input, and the difference is
   0 on every input the contract covers. Measured on the exact-start cases (below): 0 of 163 answered cases differ.
   Starts that breach the budget by a tolerance-level amount are refused by the reference and are outside the contract
   (ruling 35); r04 and the reference agree on every start the contract allows.
7. **r05 (turnover-total slackness term zeroed).** The reference's term is `kappa * (sum|d_i| - tau)`, the entry
   `sum(t) - tau` inside the complementary-slackness products (reference.py:290-300). Let `kappa > 0`. Then some sign-form
   row has `eta_s > 0` (kappa is the sum of the sign-form multipliers, and each is non-negative by F2). That row is
   in the working set, so by F5 `sum|d_i| = tau` and the entry is exactly 0. If `kappa = 0` the product is 0 for the same
   reason. So the reference's term is 0 on every output, and the mutant reports the same certificate.
8. **v10_02 (complementary slackness signed, not absolute).** Every product `m_k g_k` in the reference's maximum is
   exactly 0 on every output, so the absolute value and the signed value both equal 0:
   - Box and sector pairs. A row with a non-zero multiplier is in the working set (F2), and its slack is exactly 0 (F3),
     so its gap `g_k` is 0 and the product is 0. A row outside the working set has multiplier 0.
   - Turnover plus and minus pairs. `g_plus_i = d_i - t_i` is 0 when `d_i >= 0`, and `2 d_i < 0` when `d_i < 0`. Take
     `d_i < 0`. Then `plus_i > 0` needs a sign vector `s` with `s_i = +1` and `eta_s > 0`; such a row is in the working
     set, so by F5 `s_i d_i = |d_i| > 0`, which is impossible for `d_i < 0`. Hence `plus_i = 0` and the product is 0. The
     case `d_i > 0` is symmetric for `minus_i`.
   - Total pair. `kappa * (sum|d_i| - tau)` is 0 by proof 7.
   So every product is 0, and the two reports coincide on every output.
9. **The nine moved files (r16_02 to r16_06, v16d_01 to v16d_03, s05).** Each differs from the reference only in its
   starting-portfolio handling: a tolerance in `_parse` (s05: 1e-10; the r16 and v16d files: 1e-9, as the round-16
   reference had), and in its snapping of the start. On a start the reference accepts, every snapping step is the
   identity: the start is inside its bounds, every sector sum is at most its cap, so the snap leaves `x = w0`, and
   the turnover guard compares `sum|x - w0| = 0` with `tau >= 0`. So each planted snapping change acts only on a start
   that breaches a bound, a cap or the turnover guard, and such a start is refused by the reference (F0). The tolerance
   changes act only on starts that breach the budget, a bound or a cap by at most 1e-9 (1e-10 for s05), which the
   reference also refuses. Both kinds of start are outside the contract (ruling 35). So each file agrees with the
   reference on every start the contract allows. Measured: 0 of 163 exact-start answered cases differ. Probe for s05:
   `ledgers/M7/scripts/M7-d-r16fix/probe_s05_tolerance.log` shows that s05 answers a budget breach of 5e-11 that the
   reference refuses, and refuses 5e-10 and 2e-9 as the reference does.

## Corrections to the earlier ledger records

- Round 14 (`ledgers/M7/mutant_equivalence_r14.json`): the r04 entry is retracted (its `status` and `retraction` fields).
  Its argument assumed that the budget gap is exactly zero on every reference output, but the round-14 reference
  accepted starts within 1e-9 and snapped them, so a 2e-9 gap was possible. The claim holds under the exact-start
  contract (proof 6). The other round-14 entries are unchanged.
- Round 16 (the earlier version of this file, before ruling 35): proof 6 gave a measured bound of 1.000e-09 for r04, and
  the snapping paragraph described the snap as part of the start handling. Both are superseded by F0 and proofs 6 to 9.
  The measured maximum of 1.000e-09 belonged to the tolerance-level starts that ruling 35 removes from the contract.
- The round-16 fragment's PRJ-D1-37 asked for r04 to move to `ledgers/M7/mutants/` and be killed with a B1 start
  (`w0 = [0.499999999, 0.500000002]`). Under ruling 35 that start is outside the contract, so r04 stays here.
- Round 15 (`PRJ-R15-02`): the earlier figures (9 and 23 of 400 distinguished cases, and the maxima 7.969e-11 and
  6e-7/8e-7) belong to a reference that admitted rows with slack up to 1e-9 into the initial working set; the current
  reference admits only rows with slack exactly 0 (reference.py:206).

## Evidence

- Exact-start comparison of all eighteen files with the current reference:
  `ledgers/M7/scripts/M7-d-r16fix/equiv_exact_r16fix.py` (run from the repository root with `.venv/bin/python -I`),
  output in `ledgers/M7/scripts/M7-d-r16fix/equiv_exact_r16fix.log`. On the 50 generator cases (seeds 0-49) and 400 seeded
  random probes, 163 cases are answered by both the reference and the file. Each of the eighteen files differs from the
  reference on 0 of the 163 by more than 1e-9 (largest difference 0). The "answered only by the file" column counts the
  random probes that the reference refuses and the file answers; their largest exact start breach is 5e-10 (the
  tolerance-level cases outside the contract).
- Mutation run with the nine moved files still in `ledgers/M7/mutants/`: `ledgers/M7/scripts/M7-d-r16fix/mutate_M7_0-9.log`
  (212 of 221 killed; the nine survivors are the files listed above, and s05 was the old single-change-violating copy).
- s05 probe: `ledgers/M7/scripts/M7-d-r16fix/probe_s05_tolerance.log`.
