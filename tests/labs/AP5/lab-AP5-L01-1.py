"""Lab AP5-L01-1: Shiller's Excess Volatility Test and Present Value Bounds.

SIMULATED: generates synthetic real dividend path and computes ex-post rational
price P_t^* to test Shiller's variance inequality Var(P) <= Var(P^*).
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Set seed for reproducibility
    rng = np.random.default_rng(42)
    n_years = 100
    r_const = 0.06  # constant real discount rate 6%
    g_mean = 0.015  # mean real dividend growth 1.5%
    sigma_d = 0.12  # dividend growth volatility

    # Simulate log dividend growth and levels
    delta_d = g_mean + sigma_d * rng.standard_normal(n_years)
    d = np.zeros(n_years)
    d[0] = 10.0
    for t in range(1, n_years):
        d[t] = d[t - 1] * np.exp(delta_d[t])

    # Terminal value for ex-post rational price P_T^* = D_T / (r - g)
    p_star = np.zeros(n_years)
    p_star[-1] = d[-1] / (r_const - g_mean)

    # Backward recursion: P_t^* = (P_{t+1}^* + D_{t+1}) / (1 + r)
    for t in range(n_years - 2, -1, -1):
        p_star[t] = (p_star[t + 1] + d[t + 1]) / (1.0 + r_const)

    # Rational present value price with constant discount rate: P_t = E_t[P_t^*] = D_t / (r - g)
    p_rational = d / (r_const - g_mean)

    # Observed market price P_t with time-varying discount rates / sentiment shocks
    # Real-world prices fluctuate much more violently around fundamentals
    sentiment = np.zeros(n_years)
    phi = 0.85
    sigma_s = 0.20
    for t in range(1, n_years):
        sentiment[t] = phi * sentiment[t - 1] + sigma_s * rng.standard_normal()
    p_market = p_rational * np.exp(sentiment)

    # Compute sample volatilities
    std_p_star = float(np.std(p_star, ddof=1))
    std_p_rational = float(np.std(p_rational, ddof=1))
    std_p_market = float(np.std(p_market, ddof=1))

    # Variance ratio: Var(P_market) / Var(P_star)
    var_ratio = (std_p_market**2) / (std_p_star**2)
    violates_bound = bool(std_p_market > std_p_star)

    print("Shiller (1981) Excess Volatility Test")
    print(f"Sample length T:             {n_years} years")
    print(f"Constant discount rate R:    {r_const * 100:.2f}%")
    print(f"Mean dividend growth g:      {g_mean * 100:.2f}%")
    print(f"Std dev of rational P*:      ${std_p_star:.2f}")
    print(f"Std dev of constant-R P:     ${std_p_rational:.2f}")
    print(f"Std dev of market P:         ${std_p_market:.2f}")
    print(f"Variance ratio Var(P)/Var(P*): {var_ratio:.4f}")
    print(f"Violates Shiller bound:      {violates_bound}")


main()
