# SC1 open items

## L06: path-level reflection principle not proved (recorded deviation from the plan)

- Plan reference: `plans/SC1-build-plan.md` §3, L06 mandatory content, "the reflected path after τ_a is a Brownian motion (Assuming A3)".
- What the page does: `course/modules/SC/SC1/L06.html` proves only the fixed-time law (Proposition 2.3). Definition 2.2 states the path-level claim, labelled as a conjecture of that page, and Remark 2.4 says it is not used and not claimed.
- Reason: a path-level proof needs the finite-dimensional vectors of the reflected path to match those of B. Its post-τ_a part relies on τ_a being finite, and the page does not establish that finiteness (L06 "Infinite hitting times", L08 is the forward reference). The fixed-time argument does not cover the whole path.
- Status: open. The path-level statement can be proved after τ_a < ∞ is established (Lesson 8), by the finite-dimensional comparison with the symmetric increment after τ_a, under A3.
