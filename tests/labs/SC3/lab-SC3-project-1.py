"""Lab 1 · Worked example: Margrabe exchange option pricing and Monte Carlo verification on seed 0.

An exchange option gives the holder the right to exchange asset 2 for asset 1, payoff max(S_1(T) - S_2(T), 0).
On seed 0 (SIMULATED), parameters are:
    S_1 = 113.777, S_2 = 110.318, sigma_1 = 0.234, sigma_2 = 0.202, rho = 0.014,
    q_1 = 0.026, q_2 = 0.041, T = 0.955, r = 0.039.
By Margrabe (1978), using asset 2 as numeraire yields relative volatility:
    sigma_M = sqrt(sigma_1^2 - 2 * rho * sigma_1 * sigma_2 + sigma_2^2) = 0.306917
and closed-form price V_0 = 15.538676.
This lab computes the exact closed-form price, simulates 5,000 bivariate paths under the risk-neutral measure Q,
and confirms that the simulated price 15.637391 matches the analytical price within 2 standard errors (se = 0.305782).
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def main() -> None:
    # Seed 0 instance parameters (SIMULATED)
    s1 = 113.777
    s2 = 110.318
    sig1 = 0.234
    sig2 = 0.202
    rho = 0.014
    q1 = 0.026
    q2 = 0.041
    t = 0.955
    r = 0.039
    n_paths = 5000
    seed = 0

    # Margrabe closed-form price
    sig_m = math.sqrt(sig1**2 - 2.0 * rho * sig1 * sig2 + sig2**2)
    f1 = s1 * math.exp(-q1 * t)
    f2 = s2 * math.exp(-q2 * t)
    sq_t = math.sqrt(t)
    d1 = (math.log(f1 / f2) + 0.5 * (sig_m**2) * t) / (sig_m * sq_t)
    d2 = d1 - sig_m * sq_t
    exact_price = f1 * norm_cdf(d1) - f2 * norm_cdf(d2)

    # 2D Monte Carlo simulation under Q
    rng = random.Random(seed)
    drift1 = (r - q1 - 0.5 * (sig1**2)) * t
    vol1 = sig1 * sq_t
    drift2 = (r - q2 - 0.5 * (sig2**2)) * t
    vol2 = sig2 * sq_t
    df = math.exp(-r * t)

    payoffs: list[float] = []
    for _ in range(n_paths):
        z1 = rng.gauss(0.0, 1.0)
        z2 = rng.gauss(0.0, 1.0)
        w1 = z1
        w2 = rho * z1 + math.sqrt(1.0 - rho**2) * z2

        s1_t = s1 * math.exp(drift1 + vol1 * w1)
        s2_t = s2 * math.exp(drift2 + vol2 * w2)
        payoffs.append(df * max(s1_t - s2_t, 0.0))

    mc_price = sum(payoffs) / n_paths
    var_mc = sum((x - mc_price) ** 2 for x in payoffs) / (n_paths - 1)
    se_mc = math.sqrt(var_mc / n_paths)

    print(f"seed 0 parameters: S1={s1:.3f}, S2={s2:.3f}, sig1={sig1:.3f}, sig2={sig2:.3f}, rho={rho:.3f}")
    print(f"Margrabe volatility sigma_M: {sig_m:.6f}")
    print(f"analytical Margrabe price: {exact_price:.6f}")
    print(f"Monte Carlo price: {mc_price:.6f} (se {se_mc:.6f})")
    print(f"absolute difference: {abs(mc_price - exact_price):.6f}")
    print("simulation within 2*se of analytical price:", abs(mc_price - exact_price) <= 2.0 * se_mc)


main()
