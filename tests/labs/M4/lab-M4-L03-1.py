"""M4 lab L03: standardized third and fourth moments, computed exactly, then a seeded sample check.

Standard library only (fractions, math, random). The skewed law is a stated table: values 0, 1, 2 and 10 with
probabilities 1/2, 1/4, 1/8 and 1/8. Its central moments m_k = E[(X - mu)^k] are exact rationals. The
standardized skewness is E[Z^3] with Z = (X - mu)/sigma, which equals m3 / m2^(3/2); its square is the
exact rational m3^2 / m2^3, and the kurtosis E[Z^4] equals m4 / m2^2 exactly. The program checks the
moment formulas against a two-point Bernoulli law with p = 1/10, where the closed forms (1 - 2p)^2 / (pq) for the
squared skewness and (1 - 3pq) / (pq) for the kurtosis are derived on the lesson page, with q = 1 - p.
Last, it draws 20000 seeded values (seed 2026) from the skewed law and prints the sample skewness and
kurtosis, using the population form of each moment with divisor n. A sample is one random run. Its
values are estimates that a different seed would move, and the exact values printed above them are not.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence
from fractions import Fraction

Law = Sequence[tuple[int, Fraction]]

SKEWED: tuple[tuple[int, Fraction], ...] = (
    (0, Fraction(1, 2)),
    (1, Fraction(1, 4)),
    (2, Fraction(1, 8)),
    (10, Fraction(1, 8)),
)
WEIGHTS = (4, 2, 1, 1)  # integer weights proportional to 1/2, 1/4, 1/8, 1/8
SEED = 2026
N_DRAWS = 20000


def check_law(law: Law) -> None:
    """Raise ValueError unless every probability lies in [0, 1] and the probabilities sum to exactly 1."""
    if any(p < 0 or p > 1 for _, p in law):
        raise ValueError("each probability must lie in [0, 1]")
    if sum((p for _, p in law), Fraction(0)) != 1:
        raise ValueError("probabilities must sum to exactly 1")


def mean(law: Law) -> Fraction:
    """E[X] for a finite law."""
    return sum((v * p for v, p in law), Fraction(0))


def central_moment(law: Law, k: int) -> Fraction:
    """m_k = E[(X - mu)^k] for an integer k >= 2, exact."""
    mu = mean(law)
    return sum(((v - mu) ** k * p for v, p in law), Fraction(0))


def bernoulli(p: Fraction) -> tuple[tuple[int, Fraction], ...]:
    """The law with P(X = 1) = p and P(X = 0) = 1 - p."""
    return ((0, 1 - p), (1, p))


def sample_central_moments(xs: Sequence[int]) -> tuple[float, float, float]:
    """Sample m2, m3 and m4 about the sample mean, each with divisor n."""
    n = len(xs)
    mu = sum(xs) / n
    m2 = sum((x - mu) ** 2 for x in xs) / n
    m3 = sum((x - mu) ** 3 for x in xs) / n
    m4 = sum((x - mu) ** 4 for x in xs) / n
    return m2, m3, m4


def main() -> None:
    check_law(SKEWED)
    mu = mean(SKEWED)
    m2 = central_moment(SKEWED, 2)
    m3 = central_moment(SKEWED, 3)
    m4 = central_moment(SKEWED, 4)
    print(f"skewed law: E[X] = {mu}, Var(X) = m2 = {m2}")
    print(f"third central moment m3 = {m3}, fourth central moment m4 = {m4}")

    skew_sq = m3 * m3 / (m2 * m2 * m2)
    kurt = m4 / (m2 * m2)
    skew = float(m3) / float(m2) ** 1.5
    print(f"squared skewness m3^2 / m2^3 = {skew_sq} (exact), skewness = {skew:.4f}")
    print(f"kurtosis m4 / m2^2 = {kurt} (exact), {float(kurt):.4f}")

    p = Fraction(1, 10)
    q = 1 - p
    bern = bernoulli(p)
    bern_skew_sq = central_moment(bern, 3) ** 2 / central_moment(bern, 2) ** 3
    bern_kurt = central_moment(bern, 4) / central_moment(bern, 2) ** 2
    closed_skew_sq = (1 - 2 * p) ** 2 / (p * q)
    closed_kurt = (1 - 3 * p * q) / (p * q)
    print(
        f"Bernoulli(1/10) squared skewness {bern_skew_sq} equals (1 - 2p)^2 / (pq) = {closed_skew_sq}: "
        f"{bern_skew_sq == closed_skew_sq}"
    )
    print(f"Bernoulli(1/10) kurtosis {bern_kurt} equals (1 - 3pq) / (pq) = {closed_kurt}: {bern_kurt == closed_kurt}")

    rng = random.Random(SEED)
    values = [v for v, _ in SKEWED]
    draws = rng.choices(values, weights=WEIGHTS, k=N_DRAWS)
    s2, s3, s4 = sample_central_moments(draws)
    print(
        f"skewed law sample, seed {SEED}, n = {N_DRAWS}: skewness {s3 / math.pow(s2, 1.5):.3f}, "
        f"kurtosis {s4 / (s2 * s2):.3f}"
    )
    print(f"exact skewness {skew:.3f} and exact kurtosis {float(kurt):.3f} for the same law")


main()
