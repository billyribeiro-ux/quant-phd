"""Lab 1 · Variance Swap Static Replication & Discrete Grid Error.

This lab implements the Demeterfi, Derman, Kamal & Zou (1999) static replication
of the log contract using a portfolio of out-of-the-money European puts and calls
weighted inversely by strike squared (1/K^2). Evaluates continuous theoretical
variance against discrete option portfolios across varying strike spacings dK
and strike cutoffs [K_min, K_max] on seed 42 (SIMULATED).
"""

from __future__ import annotations

import math


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call_price(s: float, k: float, r: float, sigma: float, t: float) -> float:
    """Analytical Black-Scholes call price."""
    if t <= 1e-12 or sigma <= 1e-12:
        return max(0.0, s - k * math.exp(-r * t))
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    return s * norm_cdf(d1) - k * math.exp(-r * t) * norm_cdf(d2)


def bs_put_price(s: float, k: float, r: float, sigma: float, t: float) -> float:
    """Analytical Black-Scholes put price."""
    if t <= 1e-12 or sigma <= 1e-12:
        return max(0.0, k * math.exp(-r * t) - s)
    d1 = (math.log(s / k) + (r + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    d2 = d1 - sigma * math.sqrt(t)
    return k * math.exp(-r * t) * norm_cdf(-d2) - s * norm_cdf(-d1)


def replicate_variance(
    s0: float,
    r: float,
    sigma: float,
    t: float,
    k_min: float,
    k_max: float,
    dk: float,
) -> float:
    """Discrete static replication of annualized variance using 1/K^2 weighted options."""
    forward = s0 * math.exp(r * t)
    s_star = forward  # ATM cutoff strike

    # Discrete strike grid
    n_strikes = round((k_max - k_min) / dk) + 1
    strikes = [k_min + i * dk for i in range(n_strikes)]

    integral_puts = 0.0
    integral_calls = 0.0

    for k in strikes:
        if k < s_star:
            # Out-of-the-money put
            p = bs_put_price(s0, k, r, sigma, t)
            integral_puts += (dk / (k * k)) * p
        elif k > s_star:
            # Out-of-the-money call
            c = bs_call_price(s0, k, r, sigma, t)
            integral_calls += (dk / (k * k)) * c

    # Demeterfi et al. (1999) fair variance swap strike formula:
    # K_var = (2 / T) * exp(r * T) * [int_0^S* (1/K^2) P(K) dK + int_S*^inf (1/K^2) C(K) dK]
    k_var = (2.0 / t) * math.exp(r * t) * (integral_puts + integral_calls)
    return k_var


def main() -> None:
    print("=== Demeterfi et al. (1999) Variance Swap Static Replication ===")
    s0 = 100.0
    r = 0.03
    sigma = 0.20
    t = 0.25  # 3-month variance swap
    true_var = sigma * sigma  # 0.040000

    print(f"Underlying S0={s0:.1f}, r={r:.4f}, True Flat Vol={sigma:.4f}, True Variance={true_var:.6f}, T={t:.2f} yr")

    print("\n1. Impact of Strike Spacing dK (K_min=20, K_max=250):")
    print("   dK | Replicated Var | Error (bps) | Replicated Vol ")
    print("-----------------------------------------------------")
    for dk in [0.5, 1.0, 2.5, 5.0, 10.0]:
        rep_var = replicate_variance(s0, r, sigma, t, k_min=20.0, k_max=250.0, dk=dk)
        err_bps = (rep_var - true_var) * 10000.0
        rep_vol = math.sqrt(max(0.0, rep_var))
        print(f" {dk:4.1f} |    {rep_var:10.6f} |  {err_bps:10.4f} |    {rep_vol:10.4f} ")

    print("\n2. Impact of Strike Truncation Bounds (dK=1.0):")
    print(" [K_min, K_max] | Replicated Var | Truncation Error (bps) ")
    print("----------------------------------------------------------")
    truncations = [
        (80.0, 120.0),
        (60.0, 150.0),
        (40.0, 180.0),
        (20.0, 220.0),
        (10.0, 300.0),
    ]
    for k_min, k_max in truncations:
        rep_var = replicate_variance(s0, r, sigma, t, k_min=k_min, k_max=k_max, dk=1.0)
        err_bps = (rep_var - true_var) * 10000.0
        print(f" [{k_min:5.1f}, {k_max:5.1f}] |    {rep_var:10.6f} |        {err_bps:12.4f} ")


main()
