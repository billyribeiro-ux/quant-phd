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
