"""Lab S1-L01-1: Exact bias of sample variance estimators with divisor n and n - 1.

Enumerates all samples of size n = 2 from a three-point discrete law using fractions.Fraction.
Standard library only. No external imports.
"""

from __future__ import annotations

import itertools
from fractions import Fraction

# Three-point distribution: values and exact rational probabilities
OUTCOMES = [
    (Fraction(0), Fraction(1, 2)),
    (Fraction(1), Fraction(1, 3)),
    (Fraction(3), Fraction(1, 6)),
]


def main() -> None:
    # Population moments
    mu = sum(x * p for x, p in OUTCOMES)
    sigma2 = sum((x - mu) ** 2 * p for x, p in OUTCOMES)

    print(f"population mean: {mu} ({float(mu):.6f})")
    print(f"population variance: {sigma2} ({float(sigma2):.6f})")

    # Enumerate all 9 pairs of samples of size n = 2
    n = 2
    e_s_biased = Fraction(0)
    e_s_unbiased = Fraction(0)

    for (x1, p1), (x2, p2) in itertools.product(OUTCOMES, repeat=n):
        prob = p1 * p2
        mean = (x1 + x2) / n
        s_biased = ((x1 - mean) ** 2 + (x2 - mean) ** 2) / n
        s_unbiased = ((x1 - mean) ** 2 + (x2 - mean) ** 2) / (n - 1)

        e_s_biased += s_biased * prob
        e_s_unbiased += s_unbiased * prob

    bias_n = e_s_biased - sigma2
    bias_n_minus_1 = e_s_unbiased - sigma2

    print(f"E[S_n^2] (divisor n): {e_s_biased} ({float(e_s_biased):.6f})")
    print(f"bias of S_n^2: {bias_n} ({float(bias_n):.6f})")
    print(f"E[S_{{n-1}}^2] (divisor n - 1): {e_s_unbiased} ({float(e_s_unbiased):.6f})")
    print(f"bias of S_{{n-1}}^2: {bias_n_minus_1} ({float(bias_n_minus_1):.6f})")
    print(f"ratio E[S_n^2] / sigma^2: {e_s_biased / sigma2} (expected (n-1)/n = 1/2)")


main()
