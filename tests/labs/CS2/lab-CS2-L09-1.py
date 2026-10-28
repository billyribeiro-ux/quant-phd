"""CS2 L09 lab 1: Welford's one-pass update against two-pass and naive variance, on streams with a large offset.

Claim checked: for the same stream of n = 2000 values, the sample variance from Welford's update, from the
two-pass formula and from the naive sum-of-squares formula is compared with an exact Fraction reference.
The stream is offset + u, where u is uniform on [0, 1) from random.Random(SEED). The offset is the
variable under test: 0, 1e6 and 1e9. SIMULATED data, not market data.
Each estimate is printed in scientific notation with six digits after the decimal point. Relative error is
|estimate - exact| / exact, printed in scientific notation with three digits after the decimal point.
Standard library only.
No randomness outside the seeded generator and no network access.
"""

from __future__ import annotations

import random
from fractions import Fraction

N = 2000
SEED = 90
OFFSETS = (0.0, 1e6, 1e9)


def stream(offset: float) -> list[float]:
    """Return N values offset + u, with u drawn uniformly from [0, 1) by a generator seeded with SEED."""
    rng = random.Random(SEED)
    return [offset + rng.random() for _ in range(N)]


def welford_variance(xs: list[float]) -> float:
    """One pass: keep the count, the running mean and the running sum of squared deviations."""
    count = 0
    mean = 0.0
    sum_sq_dev = 0.0
    for x in xs:
        count += 1
        delta = x - mean
        mean += delta / count
        sum_sq_dev += delta * (x - mean)
    return sum_sq_dev / (count - 1)


def two_pass_variance(xs: list[float]) -> float:
    """Two passes: the mean first, then the sum of squared deviations from that mean."""
    mean = sum(xs) / len(xs)
    return sum((x - mean) ** 2 for x in xs) / (len(xs) - 1)


def naive_variance(xs: list[float]) -> float:
    """One pass with running sums: (sum of x squared minus (sum of x)^2 / n) / (n - 1)."""
    total = 0.0
    total_sq = 0.0
    for x in xs:
        total += x
        total_sq += x * x
    n = len(xs)
    return (total_sq - total * total / n) / (n - 1)


def exact_variance(xs: list[float]) -> Fraction:
    """The sample variance of the float values in exact Fraction arithmetic (each float converts exactly)."""
    values = [Fraction(x) for x in xs]
    n = len(values)
    mean = sum(values, Fraction(0)) / n
    return sum(((x - mean) ** 2 for x in values), Fraction(0)) / (n - 1)


def relative_error(estimate: float, exact: Fraction) -> float:
    """Return |estimate - exact| / exact, computed in exact arithmetic and returned as a float."""
    return float(abs(Fraction(estimate) - exact) / exact)


def main() -> None:
    methods = (("Welford", welford_variance), ("two-pass", two_pass_variance), ("naive", naive_variance))
    for offset in OFFSETS:
        xs = stream(offset)
        exact = exact_variance(xs)
        print(f"offset {offset!r}: exact sample variance {float(exact):.6f}")
        for name, method in methods:
            estimate = method(xs)
            print(f"  {name:<9} estimate {estimate:.6e}  relative error {relative_error(estimate, exact):.3e}")


main()
