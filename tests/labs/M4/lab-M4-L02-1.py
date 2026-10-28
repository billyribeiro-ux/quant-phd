"""M4 lab L02: expectation and variance of two finite laws, computed exactly, then a seeded sample check.

Standard library only (fractions, random). The two laws are stated tables, not data: a fair six-sided
die (values 1 to 6, each with probability 1/6) and a two-point loss in integer cents (a loss of 250000
cents with probability 1/20, and no loss otherwise). Expectations and variances are exact rationals or
integers. Each variance is computed two ways, from the definition E[(X - mu)^2] and from the shortcut
E[X^2] - mu^2, and the program checks that the two agree. It also checks the scale rule
Var(2X) = 4 Var(X) on the die. Last, it draws seeded samples (seed 2026 for the die, seed 2027 for the
loss) and prints their sample means and variances, and for the loss the number of losses and their total.
A sample is one random run, so its printed values are estimates that depend on the seed; the exact
values above them do not.
"""

from __future__ import annotations

import math
import random
from collections.abc import Sequence
from fractions import Fraction

Law = Sequence[tuple[int, Fraction]]

DIE: tuple[tuple[int, Fraction], ...] = tuple((k, Fraction(1, 6)) for k in range(1, 7))
LOSS: tuple[tuple[int, Fraction], ...] = ((0, Fraction(19, 20)), (250000, Fraction(1, 20)))
SEED_DIE = 2026
SEED_LOSS = 2027
N_DRAWS = 10000


def check_law(law: Law) -> None:
    """Raise ValueError unless every probability lies in [0, 1] and the probabilities sum to exactly 1."""
    if any(p < 0 or p > 1 for _, p in law):
        raise ValueError("each probability must lie in [0, 1]")
    if sum((p for _, p in law), Fraction(0)) != 1:
        raise ValueError("probabilities must sum to exactly 1")


def expectation(law: Law) -> Fraction:
    """E[X] = sum of x times P(X = x), over the finite support."""
    return sum((v * p for v, p in law), Fraction(0))


def second_moment(law: Law) -> Fraction:
    """E[X^2] = sum of x^2 times P(X = x)."""
    return sum((v * v * p for v, p in law), Fraction(0))


def variance_by_definition(law: Law) -> Fraction:
    """Var(X) = E[(X - mu)^2], with mu = E[X]."""
    mu = expectation(law)
    return sum(((v - mu) ** 2 * p for v, p in law), Fraction(0))


def variance_shortcut(law: Law) -> Fraction:
    """Var(X) = E[X^2] - mu^2."""
    mu = expectation(law)
    return second_moment(law) - mu * mu


def scaled(law: Law, a: int) -> Law:
    """The law of aX for an integer a: each value multiplied by a, with its probability unchanged."""
    return tuple((a * v, p) for v, p in law)


def sample_mean_and_variance(xs: Sequence[int]) -> tuple[float, float]:
    """Sample mean and sample variance with divisor n (the population form of the variance, as in Var above)."""
    n = len(xs)
    mean = sum(xs) / n
    variance = sum((x - mean) ** 2 for x in xs) / n
    return mean, variance


def main() -> None:
    check_law(DIE)
    check_law(LOSS)

    mu_die = expectation(DIE)
    var_die = variance_by_definition(DIE)
    print(f"fair die: E[X] = {mu_die}, E[X^2] = {second_moment(DIE)}, Var(X) = {var_die}")
    print(f"definition and shortcut agree for the die: {var_die == variance_shortcut(DIE)}")
    print(
        f"Var(2X) = {variance_by_definition(scaled(DIE, 2))}, which equals 4 Var(X): "
        f"{variance_by_definition(scaled(DIE, 2)) == 4 * var_die}"
    )

    mu_loss = expectation(LOSS)
    var_loss = variance_by_definition(LOSS)
    print(f"two-point loss in cents: E[X] = {mu_loss}, E[X^2] = {second_moment(LOSS)}, Var(X) = {var_loss}")
    print(f"definition and shortcut agree for the loss: {var_loss == variance_shortcut(LOSS)}")
    print(f"standard deviation of the loss in cents: {math.sqrt(var_loss):.2f}")

    rng_die = random.Random(SEED_DIE)
    rolls = [rng_die.randint(1, 6) for _ in range(N_DRAWS)]
    mean_die, var_sample_die = sample_mean_and_variance(rolls)
    print(f"die sample, seed {SEED_DIE}, n = {N_DRAWS}: mean {mean_die:.3f}, variance {var_sample_die:.3f}")
    print(f"sample mean minus 7/2: {mean_die - 3.5:+.3f}")

    rng_loss = random.Random(SEED_LOSS)
    losses = [250000 if rng_loss.random() < 0.05 else 0 for _ in range(N_DRAWS)]
    mean_loss, var_sample_loss = sample_mean_and_variance(losses)
    count = sum(1 for x in losses if x > 0)
    print(f"loss sample, seed {SEED_LOSS}, n = {N_DRAWS}: losses {count}, total {sum(losses)} cents")
    print(f"sample mean loss {mean_loss:.1f} cents, sample variance {var_sample_loss:.1f} cents squared")


main()
