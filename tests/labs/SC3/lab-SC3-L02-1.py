"""Lab 1 · The market price of risk and discounted asset martingality.

In the Black-Scholes market, the risky asset follows dS_t = mu * S_t * dt + sigma * S_t * dB_t.
With risk-free rate r, the discounted asset S*_t = exp(-r*t) * S_t has physical drift (mu - r).
The market price of risk is lambda = (mu - r) / sigma.
By Girsanov's theorem, changing measure with density Z_t = exp(-lambda * B_t - (1/2) * lambda^2 * t)
eliminates the excess drift, rendering S*_t a Q-martingale: E^Q[S*_t] = S_0 for all t >= 0.
This lab simulates 10,000 asset paths (SIMULATED) under physical measure P and verifies that
the discounted asset exhibits positive drift under P but zero drift under Q within sampling error.
"""

from __future__ import annotations

import math
import random


def main() -> None:
    seed = 42
    rng = random.Random(seed)
    n_paths = 10000
    s0 = 100.0
    mu = 0.08
    sigma = 0.20
    r = 0.03
    horizon = 1.0

    # Market price of risk
    lambda_mpr = (mu - r) / sigma
    sq_h = math.sqrt(horizon)

    # Physical theoretical discounted expectation: S_0 * exp((mu - r) * H)
    target_p_disc = s0 * math.exp((mu - r) * horizon)
    target_q_disc = s0

    s_star_vals: list[float] = []
    weighted_s_star: list[float] = []

    for _ in range(n_paths):
        b_h = sq_h * rng.gauss(0.0, 1.0)
        # S_H under physical measure P
        s_h = s0 * math.exp((mu - 0.5 * (sigma**2)) * horizon + sigma * b_h)
        # Discounted asset price S*_H = exp(-r * H) * S_H
        s_star = math.exp(-r * horizon) * s_h
        # Radon-Nikodym weight Z_H
        z = math.exp(-lambda_mpr * b_h - 0.5 * (lambda_mpr**2) * horizon)

        s_star_vals.append(s_star)
        weighted_s_star.append(z * s_star)

    # Physical expectation E^P[S*_H]
    mean_p = sum(s_star_vals) / n_paths
    var_p = sum((x - mean_p) ** 2 for x in s_star_vals) / (n_paths - 1)
    se_p = math.sqrt(var_p / n_paths)

    # Risk-neutral expectation E^Q[S*_H] = E^P[Z * S*_H]
    mean_q = sum(weighted_s_star) / n_paths
    var_q = sum((x - mean_q) ** 2 for x in weighted_s_star) / (n_paths - 1)
    se_q = math.sqrt(var_q / n_paths)

    print(f"market price of risk lambda: {lambda_mpr:.4f}")
    print(f"E^P[S*_H]: {mean_p:.4f} (target {target_p_disc:.4f}, se {se_p:.4f})")
    print(f"E^Q[S*_H]: {mean_q:.4f} (target {target_q_disc:.4f}, se {se_q:.4f})")
    print("P-expectation inside 3*se:", abs(mean_p - target_p_disc) <= 3.0 * se_p)
    print("Q-martingale property |E^Q[S*] - S0| <= 3*se:", abs(mean_q - target_q_disc) <= 3.0 * se_q)


main()
