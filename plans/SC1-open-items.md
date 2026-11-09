# SC1 open items

## L06: path-level reflection principle (closed in round 13: proved as Proposition 2.7)

- Plan reference: `plans/SC1-build-plan.md` §3, L06 mandatory content, "the reflected path after τ_a is a Brownian motion (Assuming A3)".
- What the page does now: `course/modules/SC/SC1/L06.html` Proposition 2.7 proves the path-level statement, assuming A3 (applied only to the bounded times τ_a∧t) and A4(b), A4(c), A4(g), A4(h). Proposition 2.3 is the fixed-time form. Definition 2.2 and Remark 2.4 point to Proposition 2.7.
- Reason it was open before: the earlier draft applied A3 to τ_a without showing it bounded, and assumed τ_a < ∞ was needed. The truncation at τ_a∧t avoids both: the fixed-horizon identity W_s = 2B_{s∧ρ} − B_s with ρ = τ_a∧t gives the finite-dimensional laws on [0,t] for every t.
- Status: closed for SC1 (no architect deviation recorded). The claim does not use that τ_a is finite; the page does not establish that finiteness (Lesson 8 does).

## Ruling 21: plan sections 5.5 and 5.7(4) amended (FINAL-ARCHITECT-RULINGS 21)

- Plan reference: `plans/SC1-build-plan.md` §5.5 (the `discrete_max_exceedance` test bullet) and §5.7(4). Both are amended in the plan to say what ruling 21 records. Ruling 21 text: `plans/FINAL-ARCHITECT-RULINGS.md`, item 21.
- What the built page and grader do: `course/modules/SC/SC1/grader/test_project.py` checks the one-step estimate against `reflection_tail(a, H)/2` within `simulation_band` (5 target standard errors plus 1/N), for seed 0 and the second seed (the one-step tests). It checks the grid estimate one-sided, at most `reflection_tail(a, H)` plus the same band, at `n_steps` 4 and at the instance's `n_steps`. `course/modules/SC/SC1/project.html` states that an implementation drawing the same values in a different order fails the tests, and the suite enforces that statement.
- Consequence for the alternatives: a Box–Muller alternative on a different draw order (plan §5.7(4)) cannot pass the suite the page describes, so it is not carried. The five verified alternatives are the same-order set `alt_r17_*` in `ledgers/SC1/scripts/SC1-d-r17/alternatives/`.
- Status: recorded by the architect as ruling 21. No code change is part of this record. The rounds 1-7 Box–Muller files are not in the verified set.
