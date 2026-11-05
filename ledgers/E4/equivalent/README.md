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

# Stop-rule variants (round 8 fixer)

These two files differ from `reference.py` only in the bisection loop of `solve_model`. The page states the stop rule
(project.html, Constraints: stop when the bracket is narrower than 1e-12 times its upper end, or after 200 halvings;
the reported fraction lies in the final bracket). Both variants keep the sign-change invariant, so the root stays in the
bracket. Each passes the whole suite on seeds 0 to 49 (run this round), so no output test separates them from the reference.

## `mutant_r6_08_reports_lower_end.py`: reports the lower end of the final bracket

One edit: `lam = low` in place of `lam = 0.5 * (low + high)`.

Proof that the outputs differ only inside the stated tolerance. The variant runs the same bisection as the reference,
with the same gap signs, so both end with the same bracket `[low, high]`. The reference reports its midpoint and the
variant reports `low`, so the two differ by at most `high - low`. At a tolerance stop `high - low <= 1e-12 * high`. At the
200-halving cap `high - low = 2^-200` (about 6e-61). The page allows any point of the final bracket (Constraints). The suite
tolerances (1e-10 absolute on the root, 1e-8 relative on the tiny-root checks) are larger than either difference.
This is the same variant as `mutant_r7_01_reports_bracket_lower_end.py` above, re-created in round 8 and kept under its
round-6 name because the round-6 citation points here.

## `mutant_r6_09_always_200_halvings.py`: never stops early

One edit: the loop is `while steps < 200` with no relative-tolerance test.

Proof that the outputs differ only inside the stated tolerance. The variant follows the reference's path until the
reference would stop. From then on it keeps halving inside the reference's final bracket, which contains the root, so the
variant's final bracket lies inside the reference's. Both midpoints lie in that bracket, so they differ by at most the
reference's final width, which is at most `1e-12 * high` when the reference stops on tolerance. No test can see the
number of halvings: the suite checks outputs only.

Status: the variant violates the first limb of the page's stop rule (it does not stop at the tolerance), and no output
test can observe that. It is therefore a documented interpretation, not a killed mutant. The architect may either accept
it as an output-equivalent implementation or reword the stop rule so that the step count is not a stated behaviour.
