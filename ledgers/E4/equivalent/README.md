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

# `mutant_v17_02_price_slope_drops_uninformed_term.py`: equivalent within the stated tolerances (round 17, ruling 22)

File: `mutant_v17_02_price_slope_drops_uninformed_term.py` (moved here from `mutants/` in round 17). It is the reference
solver with one change, in `price_coefficients`: the price slope omits the uninformed term from its numerator,
`b_s = lam tau_e / denominator` in place of `b_s = (lam tau_e + (1 - lam) tau_y) / denominator`. The denominator and the
ratio `b_u / b_s = -a / (lam tau_e)` are the reference's.

## Why it is not in `mutants/`

Ruling 22 of `plans/FINAL-ARCHITECT-RULINGS.md` says the three listed gap comparisons use `1e-14 * max(1, |expected|)`,
as project.html Constraints states. With that tolerance (now in `grader/test_project.py`), this variant still passes every
test on seeds 0 to 49 (50/50). Its outputs differ from the reference only inside the stated tolerances: the informed
fraction by a relative 1e-12 (the page requires 1e-10), and the reported gap is within 1e-14 of the Proposition 3 gap at
its own reported fraction (the page requires 1e-14). Ruling 22 makes such a mutant equivalent, with this proof.

The variant does break a formula that the page states (the `b_s` of Proposition 1, project.html). Only its outputs are
equal to the reference's, which is the basis of ruling 22. The architect should know that a formula is violated here
and that the suite cannot see it.

## Proof

Write `beta` for the variant's `b_s`, `b_u = -a beta / (lam tau_e)`, and `kappa = -a / (lam tau_e)`. Then `p = beta y` with
`y = s + kappa u` for every `beta`, and `Var(y) = 1/tau_v + 1/tau_y`, because `1/tau_y = 1/tau_e + kappa^2 sd^2`.

1. **Common variance.** For any linear price `p = beta s + b_u u`, the variance of `v - p` is
   `Omega(beta) = 1/tau_v + beta^2 (1/tau_v + 1/tau_e) - 2 beta / tau_v + b_u^2 sd^2`. (From `Var(v) = 1/tau_v`,
   `Var(s) = 1/tau_v + 1/tau_e` and `Cov(v, s) = 1/tau_v`.)
2. **Informed side.** The variant uses `F_I = (V_I / Omega_I)^(1/2)` with `V_I = 1/P`, `P = tau_v + tau_e`, and
   `Omega_I = 1/P + slope^2 (1/tau_v + 1/tau_e) + b_u^2 sd^2`, where `slope = tau_e/P - beta`. Expanding `slope^2`:
   the term in `beta` is `-2 beta (tau_e/P)(1/tau_v + 1/tau_e) = -2 beta / tau_v`, because
   `(1/tau_v + 1/tau_e) = P / (tau_v tau_e)`. The constant is `1/P - 1/tau_v + (tau_e/P)^2 P/(tau_v tau_e)
   = (tau_v - P + tau_e) / (P tau_v) = 0`. So `Omega_I = Omega(beta)` identically.
3. **Uninformed side.** The variant uses `F_U = (V_U / Omega_U)^(1/2)` with `V_U = 1/(tau_v + tau_y)` and
   `Omega_U = V_U + r^2 Var(y)`, where `r = q - beta` and `q = tau_y/(tau_v + tau_y)`. Since `q Var(y) = 1/tau_v`
   and `V_U + q^2 Var(y) = 1/tau_v`, `Omega_U = 1/tau_v - 2 beta/tau_v + beta^2 Var(y) = Omega(beta)`.
4. **Sign and root.** So the variant's gap is `G'(lam) = Omega(beta)^(-1/2) H(lam)` with
   `H(lam) = V_U^(1/2) - exp(ac) V_I^(1/2)`, and the reference's gap is `G(lam) = Omega(beta*)^(-1/2) H(lam)` with
   `beta*` the reference's slope. Both have the sign of `H`, which is the sign of `tau_bar - tau_y(lam)` (Proposition 3).
   So the two gaps have the same sign at every `lam` in (0, 1], and the same zero `lam*`.
5. **Bisection.** Both searches keep the sign invariant, so each final bracket contains `lam*` and has width at most
   `1e-12` times its upper end. The reported fraction is the midpoint, so it is within that width of `lam*`, which is the
   same bound for both. Floating-point signs can disagree only where `|H|` is at rounding level, that is within about
   1e-14 of `lam*`, which is inside the bracket anyway.
6. **Reported gap.** At the reported fraction `lam_m`, the variant reports `Omega(beta)^(-1/2) H(lam_m)`, while the
   Proposition 3 gap at `lam_m` is `Omega(beta*)^(-1/2) H(lam_m)`. Their difference is
   `H(lam_m) (Omega(beta)^(-1/2) - Omega(beta*)^(-1/2))`. It is small because `H(lam_m)` is of the order of the
   distance of `lam_m` from `lam*`, which is at most `1e-12` relative. This step is measured, not bounded in closed form
   (see the numbers below).

## Measured (fixer, round 17)

Script `ledgers/E4/scripts/E4-d-fix-r17/equiv_v17_02_probe.py`, output `equiv_v17_02_probe.out` in the same directory.

- Grid of 14400 cases (`sd` 0.30 to 2.70 by `cost` 0.10 to 0.20, 120 by 120): 57 cases differ in the informed fraction
  at the float level; no case changes whether the fraction is 0, 1 or interior.
- Largest `|lam_ref - lam_mut|` over interior cases: 4.547e-13; largest relative difference: 9.890e-13 (page: 1e-10).
- Largest `|reported gap - Proposition 3 gap at the reported fraction| / max(1, |gap|)`: 4.219e-15 for the variant
  (page: 1e-14); 0 for the reference.
- Identity of step 2 and 3: worst relative `|Omega from the terms - Omega(beta)|` = 8.478e-16 over 20000 random interior
  points. Sign disagreements between the two gaps with `|gap| > 1e-13`: 0 of 20000.
- Suite: reference and alt_1 to alt_8 pass seeds 0 to 49 (50/50) with the edited suite, and so do the equivalents
  (`ledgers/E4/scripts/E4-d-fix-r17/out/run_cands_fix17.txt`). `tools/mutate_graders.py --unit E4 --seeds 0-9` gives
  133/133 killed (`out/mutate_graders_E4_0_9_fix17.txt`).
