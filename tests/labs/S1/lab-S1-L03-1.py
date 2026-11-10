"""Lab S1-L03-1: Cramer-Rao bound equality and delta-method variance check.

Computes the Bernoulli sample mean efficiency in exact rational arithmetic,
and verifies the delta-method asymptotic variance of g(p) = p^2 via seeded simulation.
SIMULATED: random draws are generated with random.Random(301).
"""

from __future__ import annotations

import math
import random
from fractions import Fraction


def main() -> None:
    # Part 1: Exact Cramer-Rao bound for Bernoulli(p)
    p_exact = Fraction(2, 5)  # p = 0.40
    n_exact = 100
    cr_bound = (p_exact * (1 - p_exact)) / n_exact
    var_mean = cr_bound  # Sample mean achieves CRLB exactly

    print(f"population parameter p: {p_exact} ({float(p_exact):.2f})")
    print(f"sample size n: {n_exact}")
    print(f"Cramer-Rao lower bound: {cr_bound} ({float(cr_bound):.8f})")
    print(f"exact variance of sample mean: {var_mean} ({float(var_mean):.8f})")
    print(f"CRLB efficiency ratio: {var_mean / cr_bound}")

    # Part 2: Delta method for transform g(p) = p^2 (SIMULATED)
    # g'(p) = 2p, so asymptotic variance of g(p_hat) is [2p]^2 * p(1-p) / n = 4 * p^3 * (1 - p) / n
    p_float = 0.40
    n = 100
    n_sims = 10_000
    seed = 301
    rng = random.Random(seed)

    g_prime = 2.0 * p_float
    var_p_hat = p_float * (1.0 - p_float) / n
    asy_var_g = (g_prime**2) * var_p_hat

    g_values: list[float] = []
    for _ in range(n_sims):
        # Count successes in n Bernoulli trials
        successes = sum(1 for _ in range(n) if rng.random() < p_float)
        p_hat = successes / n
        g_values.append(p_hat**2)

    mean_g = math.fsum(g_values) / n_sims
    sim_var_g = math.fsum((x - mean_g) ** 2 for x in g_values) / (n_sims - 1)
    ratio = sim_var_g / asy_var_g

    print(f"transform g(p) = p^2: g(p) = {p_float**2:.4f}")
    print(f"delta-method asymptotic variance: {asy_var_g:.8f}")
    print(f"simulated variance (N = {n_sims}, seed = {seed}): {sim_var_g:.8f}")
    print(f"ratio simulated / delta-method variance: {ratio:.4f}")


main()
