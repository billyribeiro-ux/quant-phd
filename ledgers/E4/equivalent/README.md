# E4 project: literal price-sign variant (not counted in mutants/)

File: `literal_price_sign.py`. It is the reference solver with one change: the noise coefficient of the linear price is
given the wrong sign, `b_u = +a b_s / (lambda tau_e)` in place of `b_u = -a b_s / (lambda tau_e)`.

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

## What the architect must decide

Either (a) keep Proposition 1's sign statement, which the suite cannot test, and record this as a known limit, or
(b) remove the sign from Proposition 1, which changes no output. The builder did not edit the proposition on its own.

# Stop-rule variants (rounds 6 to 10)

These files differ from `reference.py` only in the bisection loop of `solve_model`. Round 10 reworded the page's
Constraints (project.html): the page no longer states a stop rule, a number of halvings, or that the reported fraction
lies in the final bracket. It states one accuracy requirement instead: for an interior root, when the noise volume is at
least 1e-50 and tau-bar at least 1e-2, the reported fraction agrees with the root of Proposition 4 to within the smaller of
1e-10 and 1e-8 times the root. Each variant below keeps the sign-change invariant, so its final bracket contains the root,
and each meets that requirement on the page's domain. None is killed by the suite, because the suite checks outputs only
and the page no longer states the behaviour the variants change.

Accuracy of the reference on the domain (round 10, script `ledgers/E4/scripts/E4-d-r10/check_accuracy_r10.py`, log
`ledgers/E4/scripts/E4-d-r10/logs/check_accuracy_r10.txt`): random cases with noise volume from 1e-50 to 1e3 and cost
such that tau-bar is at least 1e-2. The largest error is 0.0084 of the allowed tolerance, so the reference has a wide
margin. The domain's lower bound makes the cap harmless: for tau-bar at least 1e-2 the root is at least 0.2 times the
noise volume, so it is at least 2e-51 when the noise volume is 1e-50, and 200 halvings leave a width of 2^-200 (about
6.2e-61), which is far below 1e-8 times that root.

## `mutant_v9_02_stop_rule_relative_to_lower_end.py`: the stop test uses the lower end (moved from `mutants/` in round 10)

One edit: the loop condition is `high - low > BISECTION_TOLERANCE * low` in place of `... * high`. Since `low <= high`,
the variant's condition holds whenever the reference's holds, and both take the same decisions, so the variant follows
the reference's path and keeps halving at least as long. Its final bracket therefore lies inside the reference's, and its
midpoint differs from the reference's by at most the reference's final width, at most `1e-12 * high`. That meets the
requirement on the page's domain. Round 10 counted it as the only survivor of the mutation gate; it is an equivalent
variant on the page's domain, so it is recorded here and not in `mutants/`.

## `mutant_r6_08_reports_lower_end.py`: reports the lower end of the final bracket

One edit: `lam = low` in place of `lam = 0.5 * (low + high)`.

The variant runs the same bisection as the reference, with the same gap signs, so both end with the same bracket
`[low, high]`. The reference reports its midpoint and the variant reports `low`, so the two differ by at most
`high - low`. At a tolerance stop `high - low <= 1e-12 * high`. At the 200-halving cap `high - low = 2^-200` (about
6.2e-61), and on the page's domain that is far below 1e-8 times the root. Both differences meet the requirement, and no
test can separate the variant from the reference. This is the same variant as
`mutant_r7_01_reports_bracket_lower_end.py` below, re-created in round 8 and kept under its round-6 name because the
round-6 citation points here.

## `mutant_r6_09_always_200_halvings.py`: never stops early

One edit: the loop is `while steps < 200` with no relative-tolerance test.

The variant follows the reference's path until the reference would stop. From then on it keeps halving inside the
reference's final bracket, which contains the root, so the variant's final bracket lies inside the reference's. Both
midpoints lie in that bracket, so they differ by at most the reference's final width, which meets the requirement on the
page's domain as above. No test can see the number of halvings: the suite checks outputs only.

Status (round 10): the page no longer states a stop rule or a step count, so this variant is output-equivalent on the
page's domain and is accepted here as equivalent. The round-9 status ("documented interpretation, not a killed mutant")
is superseded by the reworded Constraints.
