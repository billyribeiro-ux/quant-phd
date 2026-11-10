"""Lab 1 · Strike Arbitrage & Butterfly Spreads: The Non-Negative Density Condition.

Evaluates European call prices across a strike grid, tests call price convexity
C(K - dK) - 2*C(K) + C(K + dK) >= 0, and calculates the Gatheral-Jacquier density
factor g(k). Demonstrates how a non-convexity violation creates butterfly arbitrage.
All data is SIMULATED (seed 42).
"""

from __future__ import annotations

import math


def svi_derivs(k: float, a: float, b: float, rho: float, m: float, sigma: float) -> tuple[float, float, float]:
    diff = k - m
    disc = math.sqrt(diff**2 + sigma**2)
    w = a + b * (rho * diff + disc)
    w_p = b * (rho + diff / disc)
    w_pp = b * (sigma**2) / (disc**3)
    return w, w_p, w_pp


def g_factor(k: float, a: float, b: float, rho: float, m: float, sigma: float) -> float:
    w, w_p, w_pp = svi_derivs(k, a, b, rho, m, sigma)
    term1 = (1.0 - (k * w_p) / (2.0 * w)) ** 2
    term2 = (w_p**2 / 4.0) * (1.0 / w + 0.25)
    term3 = 0.5 * w_pp
    return term1 - term2 + term3


def norm_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def bs_call_price(s: float, k: float, r: float, sigma: float, tau: float) -> float:
    if tau <= 1e-12:
        return max(s - k, 0.0)
    d1 = (math.log(s / k) + (r + 0.5 * sigma**2) * tau) / (sigma * math.sqrt(tau))
    d2 = d1 - sigma * math.sqrt(tau)
    return s * norm_cdf(d1) - k * math.exp(-r * tau) * norm_cdf(d2)


def main() -> None:
    spot = 100.0
    rate = 0.03
    tau = 0.50
    fwd = spot * math.exp(rate * tau)

    # Slice 1: Arbitrage-free valid benchmark
    p_valid = {"a": 0.035, "b": 0.12, "rho": -0.30, "m": 0.02, "sigma": 0.10}

    # Slice 2: Pathological parameters inducing negative density (butterfly arbitrage)
    p_bad = {"a": 0.045, "b": 0.75, "rho": -0.65, "m": 0.0, "sigma": 0.015}

    k_evals = [-0.4, -0.2, -0.1, 0.0, 0.1, 0.2, 0.4]

    print("--- Benchmark Arbitrage-Free Slice ---")
    min_g_valid = float("inf")
    for k in k_evals:
        g = g_factor(k, **p_valid)
        if g < min_g_valid:
            min_g_valid = g
        w, _, _ = svi_derivs(k, **p_valid)
        print(f"k = {k:5.2f} | w(k) = {w:.5f} | Density Factor g(k) = {g:.5f}")

    print(f"Minimum density factor g(k) on valid slice: {min_g_valid:.5f}")
    print("Valid slice is butterfly arbitrage-free:", min_g_valid >= 0.0)

    print("\n--- Pathological Slice with Butterfly Arbitrage ---")
    min_g_bad = float("inf")
    k_min_bad = 0.0
    for k in k_evals:
        g = g_factor(k, **p_bad)
        if g < min_g_bad:
            min_g_bad = g
            k_min_bad = k
        w, _, _ = svi_derivs(k, **p_bad)
        print(f"k = {k:5.2f} | w(k) = {w:.5f} | Density Factor g(k) = {g:.5f}")

    print(f"Minimum density factor on pathological slice: {min_g_bad:.5f} at k = {k_min_bad:.2f}")
    print("Butterfly Arbitrage Detected (Density Factor < 0):", min_g_bad < 0.0)

    # Numerical butterfly spread test around negative density point
    k_center = k_min_bad
    dk = 0.02
    k1, k2, k3 = k_center - dk, k_center, k_center + dk
    strike1, strike2, strike3 = fwd * math.exp(k1), fwd * math.exp(k2), fwd * math.exp(k3)

    w1, _, _ = svi_derivs(k1, **p_bad)
    w2, _, _ = svi_derivs(k2, **p_bad)
    w3, _, _ = svi_derivs(k3, **p_bad)

    c1 = bs_call_price(spot, strike1, rate, math.sqrt(w1 / tau), tau)
    c2 = bs_call_price(spot, strike2, rate, math.sqrt(w2 / tau), tau)
    c3 = bs_call_price(spot, strike3, rate, math.sqrt(w3 / tau), tau)

    fly_cost = c1 - 2.0 * c2 + c3
    print(f"\nConstructing Butterfly Spread at Strikes [{strike1:.2f}, {strike2:.2f}, {strike3:.2f}]:")
    print(f"Call Prices: C1 = {c1:.4f}, C2 = {c2:.4f}, C3 = {c3:.4f}")
    print(f"Butterfly Spread Net Cost: {fly_cost:.6f}")
    print("Negative Butterfly Cost (Arbitrage Opportunity):", fly_cost < 0.0)


main()
