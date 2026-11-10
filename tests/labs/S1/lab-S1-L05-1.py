"""Lab S1-L05-1: Exact binomial statistical power curve and Type I / Type II error trade-off.

Evaluates exact power pi(p1) = P(K >= 15 | p1) and Type II error beta(p1) = 1 - pi(p1) for n = 20.
All values computed in exact rational arithmetic using fractions.Fraction.
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
    cutoff = 15  # Decision rule from L04: reject H0 when K >= 15

    # Grid of alternative values for true parameter p
    p_values = [
        Fraction(5, 10),
        Fraction(6, 10),
        Fraction(7, 10),
        Fraction(8, 10),
        Fraction(9, 10),
    ]

    print(f"sample size n: {n}, rejection region: K >= {cutoff}")
    print("exact power and Type II error across parameter values:")

    for p in p_values:
        # Power is probability of rejection under p: sum_{k=cutoff}^n P(K = k | p)
        power = sum(binom_prob(n, k, p) for k in range(cutoff, n + 1))
        beta = Fraction(1, 1) - power  # Type II error probability

        is_null = p == Fraction(1, 2)
        label = "H0 (Type I error)" if is_null else "H1"
        print(
            f"p = {p} ({float(p):.2f}) [{label}]: "
            f"power = {power} ({float(power):.6f}), "
            f"beta = {beta} ({float(beta):.6f})"
        )

    # Check relation at null: power under p0 equals achieved Type I error rate
    type_i_rate = sum(binom_prob(n, k, Fraction(1, 2)) for k in range(cutoff, n + 1))
    print(f"achieved Type I error at p = 1/2: {type_i_rate} ({float(type_i_rate):.6f})")


main()
