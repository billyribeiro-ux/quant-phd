"""Lab 1 · Analytical Black-Scholes formula vs risk-neutral Monte Carlo expectation.

Verifies the risk-neutral expectation pricing representation:
    C(S, K, r, sigma, T) = exp(-r T) E_Q[(S_T - K)^+]
    P(S, K, r, sigma, T) = exp(-r T) E_Q[(K - S_T)^+]
and exact put-call parity C - P = S - K exp(-r T).
Compares the closed-form Black-Scholes price against a 200,000-path Monte Carlo simulation
under Q with antithetic variates, verifying agreement within 2 standard errors.
"""

from __future__ import annotations

import math
import random


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_prices(s: float, k: float, r: float, sigma: float, t: float) -> tuple[float, float]:
    """Analytical European call and put prices."""
    sq_t = math.sqrt(t)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * t) / (sigma * sq_t)
    d2 = d1 - sigma * sq_t
    df = math.exp(-r * t)

    call = s * norm_cdf(d1) - k * df * norm_cdf(d2)
    put = k * df * norm_cdf(-d2) - s * norm_cdf(-d1)
    return call, put


def mc_risk_neutral_prices(
    s: float,
    k: float,
    r: float,
    sigma: float,
    t: float,
    n_pairs: int,
    seed: int,
) -> tuple[float, float, float, float]:
    """Monte Carlo pricing under Q using antithetic variates.

    Returns:
        (call_mc, call_se, put_mc, put_se)
    """
    rng = random.Random(seed)
    df = math.exp(-r * t)
    drift = (r - 0.5 * sigma**2) * t
    vol = sigma * math.sqrt(t)

    call_sum = 0.0
    call_sq = 0.0
    put_sum = 0.0
    put_sq = 0.0

    for _ in range(n_pairs):
        z = rng.gauss(0.0, 1.0)
        s1 = s * math.exp(drift + vol * z)
        s2 = s * math.exp(drift - vol * z)

        c1 = max(s1 - k, 0.0)
        c2 = max(s2 - k, 0.0)
        c_pair = 0.5 * df * (c1 + c2)
        call_sum += c_pair
        call_sq += c_pair * c_pair

        p1 = max(k - s1, 0.0)
        p2 = max(k - s2, 0.0)
        p_pair = 0.5 * df * (p1 + p2)
        put_sum += p_pair
        put_sq += p_pair * p_pair

    call_mc = call_sum / n_pairs
    call_var = (call_sq - n_pairs * call_mc**2) / (n_pairs - 1)
    call_se = math.sqrt(max(call_var, 0.0) / n_pairs)

    put_mc = put_sum / n_pairs
    put_var = (put_sq - n_pairs * put_mc**2) / (n_pairs - 1)
    put_se = math.sqrt(max(put_var, 0.0) / n_pairs)

    return call_mc, call_se, put_mc, put_se


def main() -> None:
    # Contract and market parameters (SIMULATED)
    s = 100.0
    k = 105.0
    r = 0.05
    sigma = 0.20
    t = 0.75
    n_pairs = 100000
    seed = 12345

    call_exact, put_exact = bs_prices(s, k, r, sigma, t)
    c_mc, c_se, p_mc, p_se = mc_risk_neutral_prices(s, k, r, sigma, t, n_pairs, seed)

    # Put-call parity checks
    df = math.exp(-r * t)
    parity_lhs = call_exact - put_exact
    parity_rhs = s - k * df
    parity_diff = abs(parity_lhs - parity_rhs)

    c_diff = abs(c_mc - call_exact)
    p_diff = abs(p_mc - put_exact)

    print("Risk-neutral expectation pricing under Q (SIMULATED):")
    print(f"Call: Exact = {call_exact:.6f} | MC = {c_mc:.6f} (SE = {c_se:.6f}) | Diff = {c_diff:.6f}")
    print(f"Put:  Exact = {put_exact:.6f} | MC = {p_mc:.6f} (SE = {p_se:.6f}) | Diff = {p_diff:.6f}")
    print(f"Put-call parity check: LHS={parity_lhs:.6f}, RHS={parity_rhs:.6f}, Diff={parity_diff:.2e}")
    print("Call within 2*SE:", c_diff <= 2.0 * c_se)
    print("Put within 2*SE:", p_diff <= 2.0 * p_se)
    print("Put-call parity holds to machine precision:", parity_diff < 1e-12)


main()
