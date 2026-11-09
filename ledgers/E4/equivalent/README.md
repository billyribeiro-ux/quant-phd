# E4 project: literal price-sign variant (not counted in mutants/)

File: `literal_price_sign.py`. It is the reference solver with one change: the noise coefficient of the linear price is
given the wrong sign, `b_u = +a b_s / (lambda tau_e)` in place of `b_u = -a b_s / (lambda tau_e)`. It is regenerated from
the current `grader/reference.py` in round 11 (script `ledgers/E4/scripts/E4-d-fix-r11/regen_equivalent_fix11.py`).

## Why it is not in `mutants/`

Ruling 9 of `plans/FINAL-ARCHITECT-RULINGS.md` says a mutant that differs from the reference only where the page states
nothing goes here, with a proof. This variant differs where the page does state something: Proposition 1 gives the
sign of `b_u / b_s`. No output of `solve_model` depends on that sign, so no test in the suite can kill this variant.
It is therefore recorded here as an open item for the architect, not as a surviving mutant that the suite misses.

## Proof that the three outputs do not change

1. In `reference.py`, `b_u` is read in exactly one expression: `var_gap = slope * slope * var_signal + b_u * b_u * noise_sd * noise_sd`
   (in `informed_term`). Every other use is the tuple it is returned in. `uninformed_term` unpacks it as `_`.
2. `b_u` enters only through `b_u * b_u`. Replacing `b_u` by `-b_u` leaves `b_u * b_u` unchanged in floating point,
   because negation is exact in IEEE 754 and the product of two equal magnitudes with equal signs is computed identically.
3. `informed_term`, `uninformed_term`, `indifference_gap`, `price_informativeness`, `gap_at_zero` and `solve_model` use
   no other value that depends on the sign of `b_u`. The informativeness uses only `tau_y`, and `tau_y` does not involve `b_u`.
4. Check: the variant and the reference were compared on 3000 random inputs with `noise_sd` in [0.05, 3.0] and
   `info_cost` in [0, 0.4]. The largest absolute difference in any of the three outputs was 0.0.
5. Round 11: the regenerated variant passes the suite on seeds 0 to 49 (50/50).

## What the architect must decide

Either (a) keep Proposition 1's sign statement, which the suite cannot test, and record this as a known limit, or
(b) remove the sign from Proposition 1, which changes no output. The builder did not edit the proposition on its own.

# Stop-rule variants (rounds 6 to 11)

Round 11 changed the reference and the page. The reference now takes at most 240 halvings (it was 200), and
`project.html` Constraints states the stop rule as a documented constant: the search stops when the bracket is no wider
than 1e-12 times its upper end, and at most 240 halvings are taken. The page also states the accuracy at the edge of its
domain: for a noise volume of at least 1e-50 and tau-bar of at least 1e-2, the reported fraction agrees with the root of
Proposition 4 to within 1e-10 times the root.

The 200-halving cap missed that requirement. Measured on 90000 cases in the domain's corner, a 300 by 300 grid: noise
volume 1e-50 * (1 + 0.002 i) for i = 0 to 299 (1e-50 to 1.598e-50), and cost from 0.1702992124 to 0.1707992124, which gives
tau-bar from 0.010000 to 0.012022 (script `ledgers/E4/scripts/E4-d-fix-r11/check_corner_accuracy_fix11.py`). With the cap
of 200, 11598 cases exceed 1e-10 relative, and the largest relative error is 1.5322e-10 at noise volume 1e-50 and cost
0.17076911209224613 (tau-bar 0.0101216, root 2.0224e-51; logs `ledgers/E4/scripts/E4-d-fix-r11/logs/check_corner_cap200_fix11.txt`
and `ledgers/E4/scripts/E4-d-r13/readme_corner_repro_r13.txt`). At the truncated cost 0.17076911209 the cap-200 error is
8.0e-12, so the cost is written at full digits.
With the cap of 240 the same scan has no case above 1e-10, and its largest relative error is 5.1e-13
(`ledgers/E4/scripts/E4-d-fix-r11/logs/check_corner_accuracy_fix11.txt`). A search that stops at the tolerance reaches a
width of 1e-12 times the root by about 209 halvings at a root near 2e-51, so 240 halvings are enough at every root above
about 6e-61.

## `mutant_r6_09_always_200_halvings.py`: moved to `mutants/` in round 11

The variant never applies the relative stop rule and takes 200 halvings. At a root near 2e-51 its bracket is 2^-200
(about 6.2e-61) wide, against a requirement of 1e-10 times the root (about 2.0e-61). It violates a behaviour the page now
states, and the suite kills it on the corner test (`test_corner_root_meets_the_relative_accuracy_at_the_domain_edge`,
seed 0). Its file is `ledgers/E4/mutants/mutant_r6_09_always_200_halvings.py`; the copy that was here is removed.

## Variants that are equivalent on the page's domain (round 11)

These variants differ from the reference only in the stop test or in the reported point of the final bracket. Each one
keeps the sign-change invariant, so its final bracket contains the root, and its reported fraction differs from the
reference's by at most the final bracket width, which is at most 1e-12 times the root. That is inside the page's
accuracy requirement, so no output test can separate them. Each passes the suite on seeds 0 to 49 (50/50, round 11, log
`ledgers/E4/scripts/E4-d-fix-r11/logs/equiv_0-49.txt`).

- `mutant_v9_02_stop_rule_relative_to_lower_end.py`: the stop test uses the lower end of the bracket. Since `low <= high`,
  the variant keeps halving at least as long as the reference, so its final bracket lies inside the reference's.
- `mutant_r6_08_reports_lower_end.py` and `mutant_r7_01_reports_bracket_lower_end.py` (the same edit): the reported
  fraction is the lower end of the final bracket, not its midpoint. The two differ by at most the final width.

## Decision: ruling 17 (round 16)

Ruling 17 of `plans/FINAL-ARCHITECT-RULINGS.md` (binding) settles the open item. The E4 page requires the reported root
to lie within 1e-10 times the oracle's root, and the stop rule and the midpoint report are the reference's convention.
The three variants above differ from the reference only inside the stop tolerance, so they are not student errors and
they live in this directory with ruling 17 as their proof. The page says so in one sentence (project.html, Constraints):
any reported fraction within 1e-10 times the oracle's root is accepted, whatever point of the final bracket the solver
reports.

Proof, with the reference's stop test `high - low > 1e-12 * high` (and at most 240 halvings) and its midpoint report:

1. Every variant runs the same bisection step as the reference: the same `mid`, and the same update `low = mid` or
   `high = mid` from the sign of the gap. Only the stop test or the reported point differs.
2. The invariant `0 <= low <= high` holds, and the root lies in `[low, high]` (sign change). So any point of the final
   bracket is within its width of the root.
3. `mutant_v9_02` (stop test `high - low > 1e-12 * low`): since `low <= high`, `1e-12 * low <= 1e-12 * high`. The variant
   therefore keeps halving at least as long as the reference, and its final bracket lies inside the reference's final
   bracket, whose width is at most `1e-12 * high`, about `1e-12` times the root.
4. `mutant_r6_08` and `mutant_r7_01` (report `low`, not `0.5 * (low + high)`): the reported point and the midpoint both
   lie in the reference's final bracket, so they differ by at most that width, about `1e-12` times the root.
5. Each passes the suite on seeds 0 to 49 (50/50): round 11, `ledgers/E4/scripts/E4-d-fix-r11/logs/equiv_0-49.txt`;
   round 15, `ledgers/E4/scripts/E4-d-r15/out/alternatives_equivalents_0_49.txt`.

`literal_price_sign.py` is not a stop-rule variant and is not covered by ruling 17; its proof is in the section above.

# `mutant_v17_02_price_slope_drops_uninformed_term.py`: retracted (round 18, ruling 24); back in `mutants/`

The round-17 equivalence argument for this variant is retracted. The file is back in `ledgers/E4/mutants/`, and the
suite kills it with `test_gap_at_the_domain_point_matches_proposition_3_exactly` in `grader/test_project.py`. That test
computes the gap of Proposition 3 from the Proposition 1 coefficients in 60-digit decimal arithmetic, at a domain point
where this variant misses.

## Why it is not equivalent

The variant's reported gap differs from the Proposition 3 gap at its own reported fraction by more than the page's
1e-14 precision at domain points that the round-17 grid did not cover. So ruling 22 does not apply: it covers only a
difference inside the stated tolerance.

- Sweep over the page's domain (`ledgers/E4/scripts/E4-d-r18/sweep_v17_02.py`, output
  `ledgers/E4/scripts/E4-d-r18/out/sweep_v17_02.txt`): at 1513 of 43582 interior points the variant's reported gap
  differs by more than 1e-14 relative to the larger of 1 and the gap, measured against the reference's formula at the
  same fraction. The noise volume is log-spaced from 1e-50 to 1e2 and the cost runs from 0 to 0.34. The largest
  difference is 1.57e-14, at noise volume 3.3245979322709314e-22 and cost 0.059130434782608696.
- At that point the reference's reported fraction is about 7.79e-22, and the gap at that fraction is about 7.56e-14. The
  reference's double-precision gap is within 1.2e-16 of the 80-digit exact gap. The variant's is off by -1.55e-14
  (`ledgers/E4/scripts/E4-d-r18/exact_v17_02.py`, output `ledgers/E4/scripts/E4-d-r18/out/exact_v17_02.txt`).
- The round-17 measurements (grid of noise volume 0.30 to 2.70 and cost 0.10 to 0.20, maximum 4.219e-15) are correct for
  that grid, and steps 1 to 4 of the round-17 proof (the common variance Omega(beta)) are correct. Step 6 was measured,
  not bounded, and the measurement does not extend to the page's domain.

On the autograder's box (noise volume 0.500 to 0.750, cost 0.120 to 0.150, 200 by 200 interior points) the largest
difference is 3.66e-15, inside the tolerance. That is why the checks run before round 18 did not kill the variant
(`ledgers/E4/scripts/E4-d-r18/out/sweep_v17_02.txt`, line BOX).

The variant still breaks the `b_s` formula of Proposition 1 on the page. The suite now tests that formula at a domain
point where the formula's error is visible.

# `mutant_r19_02_price_denominator_drops_uninformed_posterior_precision.py`: equivalent within the stated accuracy (round 19, ruling 25)

File: `mutant_r19_02_price_denominator_drops_uninformed_posterior_precision.py`. Student error: the denominator of the
price coefficient `b_s` (Proposition 1, `price_coefficients`, reference.py:56) uses the prior precision `tau_v` in the
uninformed part, not the uninformed posterior precision `tau_v + tau_y`. Its file was in `mutants/` and is moved here by
ruling 25 of `plans/FINAL-ARCHITECT-RULINGS.md`.

## Why it is not counted in `mutants/`

Ruling 25 says a mutant whose every output stays within the page's stated accuracy of the reference, on all inputs
searched, cannot be separated by a test the page justifies. The page states 1e-14 for the gap (ruling 22: the three
listed comparisons use `1e-14 * max(1, |expected|)`). On the searched interior points the variant's gap differs from the
exact Proposition 3 gap at its own reported fraction by at most 8.5e-15 in that measure. No searched point exceeds
1e-14, so no test in the suite can separate it at the page's accuracy. Contrast ruling 24 and `mutant_v17_02`, which
differs by up to 1.57e-14 at a domain point, beyond 1e-14, and is killed.

## The sweep (measured, not proved)

Script `ledgers/E4/scripts/E4-d-r25/sweep_r19_02_r25.py`, output `ledgers/E4/scripts/E4-d-r25/out/sweep_r19_02_r25.txt`.
It runs the reference (as `solver.py`) and this variant on random interior points, and compares each gap with the suite's
exact oracle `prop3_gap_exact` at the fraction each solver reports. The error is `|gap - exact| / max(1, |exact|)`.

| Sample | Draws | Noise volume sd | Cost c | Interior points | Variant above 1e-14 | Worst variant error |
|---|---|---|---|---|---|---|
| A (seed 7) | 20000 | 10^-8 to 10^-0.5 (log-uniform) | 0 to 0.2 | 17194 | 0 | 8.273e-15 |
| B (seed 99) | 60000 | 10^-6.5 to 10^-2.5 (log-uniform) | 0.03 to 0.12 | 60000 | 0 | 8.517e-15 |

Together 77194 interior points; the worst error is 8.517e-15 (sample B, sd 2.5548e-4, cost 0.0331606). At the variant's
worst point of each sample, the reference's own error against the same oracle is 5.7e-17 (sample A) and 3.1e-17 (sample B).

This is a measurement on a sample. It is not a proof that the variant is equivalent on the page's whole domain. The
samples do not cover noise volumes below 1e-8, the domain edge near 1e-50, or costs and noise volumes outside the two
ranges above, so the bound 1e-14 is measured, not proved, outside them. A point with error above 1e-14 at any
unsampled input would make the variant a student error, and the suite would then need a test at that point (ruling 24).

## What is algebraically exact

At `lam = 1` the uninformed part of the denominator is multiplied by `1 - lam = 0`, so the variant's `b_s` equals the
reference's at `lam = 1`, and so does the gap there (`indifference_gap(1.0)` uses only `b_s` and `tau_y`, and `tau_y` does
not depend on the denominator). The boundary rule of `solve_model` therefore decides `lam = 1` the same way for both.
This is an algebraic fact about the formula, not a sweep result. The interior fractions are not claimed equal here.

## Decision

Ruling 25 (round 19, binding for fixers and verifiers) moves this variant to `ledgers/E4/equivalent/` with this section
and the sweep as evidence. The round-19 driver `ledgers/E4/scripts/E4-d-r19/out/alts_driver.log` covers the other four
equivalents, not this variant, because it was in `mutants/` then. Its seeds 0 to 49 result from the round-25 run is in
`ledgers/E4/scripts/E4-d-r25/out/equiv_r19_02_0_49.txt`.
