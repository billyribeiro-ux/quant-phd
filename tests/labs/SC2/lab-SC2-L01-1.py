"""Lab 1 · Variance of the Itô integral for a simple step integrand.

A step integrand H_s takes constant values on intervals [t_k, t_{k+1}]. The Itô integral is defined as the sum
sum_k H_{t_k} Delta B_k. By the independence and stationarity of Brownian increments, its expectation is zero and its
variance equals sum_k H_{t_k}^2 Delta t_k exactly. This lab computes the exact rational variance with
fractions.Fraction, simulates 5,000 independent realization paths from seed 42 (SIMULATED), and checks that the sample
mean and variance agree with the theoretical values within their standard error bands.
"""

from __future__ import annotations

import math
import random
from fractions import Fraction


def main() -> None:
    # Partition of [0, 1] with 3 intervals
    t = [Fraction(0), Fraction(1, 4), Fraction(1, 2), Fraction(1)]
    dt = [t[k + 1] - t[k] for k in range(3)]
    h_vals = [Fraction(2), Fraction(-1), Fraction(3)]

    # Exact variance in Fraction
    exact_var_frac = sum(h_vals[k] ** 2 * dt[k] for k in range(3))
    exact_var_float = float(exact_var_frac)

    # Seeded Monte Carlo simulation (SIMULATED)
    seed = 42
    rng = random.Random(seed)
    n_paths = 5000
    mc_values: list[float] = []

    dt_floats = [float(d) for d in dt]
    sq_dts = [math.sqrt(d) for d in dt_floats]
    h_floats = [float(h) for h in h_vals]

    for _ in range(n_paths):
        val = sum(h_floats[k] * rng.gauss(0.0, sq_dts[k]) for k in range(3))
        mc_values.append(val)

    sample_mean = sum(mc_values) / n_paths
    sample_var = sum((x - sample_mean) ** 2 for x in mc_values) / (n_paths - 1)
    se_mean = math.sqrt(sample_var / n_paths)
    se_var = math.sqrt(2.0 * (sample_var**2) / (n_paths - 1))

    print(f"exact variance (Fraction): {exact_var_frac} = {exact_var_float:.6f}")
    print(f"sample mean: {sample_mean:.6f} (se {se_mean:.6f})")
    print(f"sample variance: {sample_var:.6f} (se {se_var:.6f})")
    print("mean inside 5*se band:", abs(sample_mean) <= 5.0 * se_mean)
    print("variance inside 5*se band:", abs(sample_var - exact_var_float) <= 5.0 * se_var)


main()
