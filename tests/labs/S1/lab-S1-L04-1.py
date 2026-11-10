"""Lab S1-L04-1: Exact binomial hypothesis test and p-value calculation.

Evaluates an exact one-sided binomial test of H0: p = 1/2 vs H1: p > 1/2 for n = 20.
All probabilities and tail sums are computed in exact rational arithmetic using fractions.Fraction.
Standard library only. No external imports.
"""

from __future__ import annotations

import math
from fractions import Fraction


def binom_prob(n: int, k: int, p: Fraction) -> Fraction:
    """Exact binomial PMF P(K = k) = comb(n, k) * p^k * (1 - p)^(n - k)."""
    comb = math.comb(n, k)
    return Fraction(comb, 1) * (p**k) * ((1 - p) ** (n - k))


def main() -> None:
    n = 20
    p0 = Fraction(1, 2)
    alpha_nominal = Fraction(5, 100)

    # Compute PMF and upper tail probabilities P(K >= c) under H0
    pmf = [binom_prob(n, k, p0) for k in range(n + 1)]
    tail = [sum(pmf[k:]) for k in range(n + 1)]

    # Find rejection cutoff: smallest integer c such that P(K >= c) <= alpha_nominal
    c_star = next(c for c in range(n + 1) if tail[c] <= alpha_nominal)
    achieved_size = tail[c_star]

    print(f"sample size n: {n}, null parameter p0: {p0}")
    print(f"nominal significance level alpha: {alpha_nominal} ({float(alpha_nominal):.4f})")
    print(f"critical cutoff c*: {c_star}")
    print(f"achieved test size alpha*: {achieved_size} ({float(achieved_size):.6f})")
    print(f"achieved size <= nominal alpha: {achieved_size <= alpha_nominal}")
    print(f"tail prob at c* - 1 ({c_star - 1}): {tail[c_star - 1]} ({float(tail[c_star - 1]):.6f}) > nominal")

    # p-value calculations for observed data
    k_obs1 = 15  # Rejects at c* = 15
    pval_1 = tail[k_obs1]
    k_obs2 = 13  # Fails to reject
    pval_2 = tail[k_obs2]

    print(f"observed k = {k_obs1}: p-value = {pval_1} ({float(pval_1):.6f}), reject H0: {pval_1 <= alpha_nominal}")
    print(f"observed k = {k_obs2}: p-value = {pval_2} ({float(pval_2):.6f}), reject H0: {pval_2 <= alpha_nominal}")


main()
