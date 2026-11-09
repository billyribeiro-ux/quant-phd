"""Check which rounding in Welford's update drives the Lab 1 error (CS2-c244 mechanism). Standard library only."""

from __future__ import annotations

import random
from fractions import Fraction

N = 2000
SEED = 90
OFFSETS = (0.0, 1e6, 1e9)


def stream(offset: float) -> list[float]:
    rng = random.Random(SEED)
    return [offset + rng.random() for _ in range(N)]


def welford_as_lab(xs: list[float]) -> float:
    count = 0
    mean = 0.0
    sum_sq_dev = 0.0
    for x in xs:
        count += 1
        delta = x - mean
        mean += delta / count
        sum_sq_dev += delta * (x - mean)
    return sum_sq_dev / (count - 1)


def welford_exact_mean(xs: list[float]) -> float:
    """Mean kept as an exact Fraction; sum of squared deviations still in float."""
    count = 0
    mean = Fraction(0)
    sum_sq_dev = 0.0
    for x in xs:
        count += 1
        fx = Fraction(x)
        delta = fx - mean
        mean += delta / count
        sum_sq_dev += float(delta * (fx - mean))
    return sum_sq_dev / (count - 1)


def welford_rounded_mean_exact_m2(xs: list[float]) -> float:
    """Mean rounded to float at each step (as the lab); sum of squared deviations kept exact."""
    count = 0
    mean = 0.0
    sum_sq_dev = Fraction(0)
    for x in xs:
        count += 1
        fx = Fraction(x)
        delta = fx - Fraction(mean)
        mean = float(Fraction(mean) + delta / count)
        sum_sq_dev += delta * (fx - Fraction(mean))
    return float(sum_sq_dev / (count - 1))


def exact_variance(xs: list[float]) -> Fraction:
    values = [Fraction(x) for x in xs]
    n = len(values)
    mean = sum(values, Fraction(0)) / n
    return sum(((x - mean) ** 2 for x in values), Fraction(0)) / (n - 1)


def rel(estimate: float, exact: Fraction) -> float:
    return float(abs(Fraction(estimate) - exact) / exact)


for offset in OFFSETS:
    xs = stream(offset)
    exact = exact_variance(xs)
    print(f"offset {offset!r}")
    print(f"  welford as lab          rel err {rel(welford_as_lab(xs), exact):.3e}")
    print(f"  welford mean exact      rel err {rel(welford_exact_mean(xs), exact):.3e}")
    print(f"  welford mean rounded, M2 exact  rel err {rel(welford_rounded_mean_exact_m2(xs), exact):.3e}")
