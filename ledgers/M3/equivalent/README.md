# M3 equivalent mutants

An equivalent mutant is a single-change copy of the reference that returns the same value as the reference for every
input. No test can kill it, so it is kept here with its proof rather than in `mutants/`.

## alt10_no_unit_diagonal_correction.py

**Change.** `projection_repair` sets the unit-diagonal correction `corr_u` to zero after every step, instead of
`corr_u = Y + corr_u - N`. Everything else is the reference.

**Claim.** For every symmetric input, every `tol` and every `max_iter`, the output is bitwise identical to the
reference's output.

**Proof.** Write the reference's iteration as in project.html (conventions, "Alternating steps"), with `H_k` the
correction term, `J_k = P(X_{k-1} + E_{k-1})`, `N_k = J_k + H_{k-1}` with every diagonal entry set to 1, and
`H_k = J_k + H_{k-1} - N_k`.

1. `H_0 = 0`, so every off-diagonal entry of `H_0` is exactly `0.0`.
2. Induction. Suppose every off-diagonal entry of `H_{k-1}` is exactly `0.0`. Then for `i != j`,
   `N_ij = J_ij + 0.0 = J_ij` in floating point, because adding `0.0` to a finite float returns that float.
3. The diagonal of `N_k` is set to 1 whatever `H_{k-1}` holds, so `N_k` equals `J_k` with its diagonal replaced by 1.
   `N_k` does not depend on the diagonal of `H_{k-1}`.
4. For `i != j`, `H_ij = J_ij + 0.0 - N_ij = J_ij - J_ij = 0.0`, which restores the induction hypothesis.
5. `H_k` is read only in `N_{k+1}`, and there only its off-diagonal entries matter, because the diagonal is then
   overwritten. The gap `||N_k - J_k||_F`, the change `||N_k - X_{k-1}||_F`, the stopping test and the output `X_k = N_k`
   do not involve `H`. So the sequence `X_k` and the stopping step are the same with `H` set to zero.

Hence the reference's unit-diagonal correction is inert on this iteration: the iteration is the plain alternating
projection with its diagonal reset to 1. The mutant removes an inert term, so it is equivalent.

**Check.** `ledgers/M3/scripts/M3-d-r7-fixer/equiv_alt10_check.py` compares the reference and this file bit for bit on
random symmetric matrices of sizes 2 to 6, for `max_iter` in {1, 2, 3, 5, 500} with `tol = 0`. Output is recorded in
`equiv_alt10_check.out` (10000 trials, outputs differing 0).

**Consequence for the page.** The correction is printed in the update of project.html but has no effect on the
output. The page does not claim that it does, so no page sentence is false; the observation is recorded here and in
the round-7 fixer report.

## Other candidates

None. Every other mutant of the M3 suite is killed (see `ledgers/M3/mutants/`). The stopping rule that stops when
either the gap or the change is at most `tol` is not equivalent (it can stop one step earlier), so it is filed as an
alternative in `ledgers/M3/alternatives/alt10_stop_when_either_gap_or_change.py`, which passes seeds 0-49.
