"""M6 L11 lab 1: Doob's maximal inequality for |S_k| of a fair walk, checked exactly.

The fair walk takes steps X_1, ..., X_N, each +1 or -1 with probability 1/2, and S_k = X_1 + ... + X_k with S_0 = 0.
The sample space is the 2**N step sequences, each with weight 2**(-N). Every probability and expectation is an
exact fractions.Fraction.

Part A: for N from 1 to 12, the process X_k = |S_k| (k = 0, ..., N) is checked against the inequality
P(max_{k<=N} X_k >= lambda) <= E[X_N] / lambda, for every lambda in the grid j/2 with j = 1, ..., 2(N+1). The lab
also checks the intermediate line lambda * P(A) <= E[X_N 1_A] <= E[X_N], where A = {max_{k<=N} X_k >= lambda}. It
prints the largest ratio lambda * P(A) / E[X_N] over the grid, the lambda where it is attained, and P(A) at that lambda.

Part B: the one-step submartingale inequality E[X_{k+1} 1_B] >= E[X_k 1_B] is checked for N = 12 on every atom B of
the first-k-steps partition. Each atom is a set of paths sharing their first k steps, and every event in that
partition is a union of atoms, so the atom check covers all of them.

Part C: the signed walk S_k is a martingale but not a nonnegative process. For N = 1 and N = 2 with lambda = 1, the
probability that max S_k >= 1 is compared with E[S_N] / lambda. The bound fails, so nonnegativity is needed.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

MAX_N = 12


def paths(length: int) -> list[tuple[int, ...]]:
    """All step sequences of the given length, each step +1 or -1."""
    return list(itertools.product((1, -1), repeat=length))


def partial_sums(path: tuple[int, ...]) -> list[int]:
    """S_0, S_1, ..., S_N for one step sequence, with S_0 = 0."""
    sums = [0]
    for step in path:
        sums.append(sums[-1] + step)
    return sums


def part_a() -> None:
    """Doob's inequality for X_k = |S_k| over the grid of lambda values, for each horizon N from 1 to 12."""
    print("Part A: P(max_{k<=N} X_k >= lambda) <= E[X_N] / lambda for X_k = |S_k|")
    for n in range(1, MAX_N + 1):
        weight = Fraction(1, 2**n)
        sample = paths(n)
        expected_last = sum((weight * abs(partial_sums(p)[n]) for p in sample), Fraction(0))
        worst_ratio = Fraction(0)
        worst_lambda = Fraction(0)
        worst_prob = Fraction(0)
        all_hold = True
        grid = [Fraction(j, 2) for j in range(1, 2 * (n + 1) + 1)]
        for lam in grid:
            hit = [p for p in sample if max(abs(s) for s in partial_sums(p)) >= lam]
            prob = weight * len(hit)
            e_hit = sum((weight * abs(partial_sums(p)[n]) for p in hit), Fraction(0))
            bound = expected_last / lam
            all_hold = all_hold and prob <= bound and lam * prob <= e_hit <= expected_last
            ratio = lam * prob / expected_last
            if ratio > worst_ratio:
                worst_ratio, worst_lambda, worst_prob = ratio, lam, prob
        print(
            f"N {n} lambda_count {len(grid)} all_bounds_hold {all_hold} "
            f"largest_ratio {float(worst_ratio):.6f} at_lambda {worst_lambda} "
            f"probability_at_lambda {worst_prob} "
            f"E_X_N {expected_last}"
        )


def part_b() -> None:
    """The one-step submartingale inequality for X_k = |S_k|, on every atom of the first-k-steps partition."""
    print("Part B: one-step submartingale inequality on every atom, N = 12")
    sample = paths(MAX_N)
    every_atom_holds = True
    atoms_checked = 0
    for k in range(MAX_N):
        atoms: dict[tuple[int, ...], int] = {}
        for p in sample:
            sums = partial_sums(p)
            gain = abs(sums[k + 1]) - abs(sums[k])
            atoms[p[:k]] = atoms.get(p[:k], 0) + gain
        atoms_checked += len(atoms)
        every_atom_holds = every_atom_holds and all(total >= 0 for total in atoms.values())
    print(f"atoms_checked {atoms_checked} one_step_submartingale_on_every_atom {every_atom_holds}")


def part_c() -> None:
    """The signed walk fails Doob's bound: its values are not nonnegative."""
    print("Part C: the signed walk S_k against the same bound, lambda = 1")
    for n in (1, 2):
        weight = Fraction(1, 2**n)
        sample = paths(n)
        prob = weight * sum(1 for p in sample if max(partial_sums(p)) >= 1)
        expected_last = sum((weight * partial_sums(p)[n] for p in sample), Fraction(0))
        print(f"N {n} P_max_signed_at_least_1 {prob} E_S_N {expected_last} bound_holds {prob <= expected_last / 1}")


def main() -> None:
    """Print Parts A, B and C."""
    part_a()
    part_b()
    part_c()


main()
