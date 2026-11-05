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

**Open item for the architect (ruling 9).** The page now states the stop rule, so these variants do violate a stated
behaviour (the stop test and the reported point). They are output-equivalent within the stated accuracy, which no
output test can distinguish. Whether "equivalent within the stated accuracy" is enough to keep them here, or whether
the page must state the reported point, is the architect's call. The fixer does not decide it.
