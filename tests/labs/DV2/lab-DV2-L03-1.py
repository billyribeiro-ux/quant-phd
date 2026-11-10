"""Lab 1 · Calendar Arbitrage & Total Variance: Monotonicity Across Expirations.

Evaluates total implied variance w(k, tau) across multiple maturities tau_1 < tau_2,
tests the monotonicity condition dw / dtau >= 0, and demonstrates calendar spread
arbitrage when term structure slices cross.
All data is SIMULATED (seed 42).
"""

from __future__ import annotations

import math


def svi_val(k: float, a: float, b: float, rho: float, m: float, sigma: float) -> float:
    diff = k - m
    disc = math.sqrt(diff**2 + sigma**2)
    return a + b * (rho * diff + disc)


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
    rate = 0.0  # Forward measure / zero interest rate setting
    t1 = 0.25
    t2 = 0.75

    # Valid calibrated slices with strictly increasing total variance
    p1 = {"a": 0.015, "b": 0.08, "rho": -0.32, "m": 0.005, "sigma": 0.06}
    p2_valid = {"a": 0.040, "b": 0.12, "rho": -0.32, "m": 0.015, "sigma": 0.09}

    # Crossed slice with lower total variance at later maturity (calendar arbitrage)
    p2_crossed = {"a": 0.010, "b": 0.07, "rho": -0.32, "m": 0.015, "sigma": 0.07}

    k_grid = [-0.4, -0.2, 0.0, 0.2, 0.4]

    print("--- Monotonic Term Structure (No Calendar Arbitrage) ---")
    min_diff_valid = float("inf")
    for k in k_grid:
        w1 = svi_val(k, **p1)
        w2 = svi_val(k, **p2_valid)
        diff = w2 - w1
        if diff < min_diff_valid:
            min_diff_valid = diff
        print(f"k = {k:5.2f} | w(T1=0.25) = {w1:.5f} | w(T2=0.75) = {w2:.5f} | Spread (w2 - w1) = {diff:.5f}")

    print(f"Minimum variance spread on valid surface: {min_diff_valid:.5f}")
    print("Valid surface is calendar arbitrage-free:", min_diff_valid >= 0.0)

    print("\n--- Crossing Term Structure (Calendar Arbitrage Detected) ---")
    min_diff_cross = float("inf")
    k_worst = 0.0
    for k in k_grid:
        w1 = svi_val(k, **p1)
        w2_c = svi_val(k, **p2_crossed)
        diff = w2_c - w1
        if diff < min_diff_cross:
            min_diff_cross = diff
            k_worst = k
        print(f"k = {k:5.2f} | w(T1=0.25) = {w1:.5f} | w(T2=0.75) = {w2_c:.5f} | Spread (w2 - w1) = {diff:.5f}")

    print(f"Minimum variance spread on crossed surface: {min_diff_cross:.5f} at k = {k_worst:.2f}")
    print("Calendar Arbitrage Detected (w2 < w1):", min_diff_cross < 0.0)

    # Financial manifestation: Calendar spread trade (buy longer, sell shorter)
    k_target = k_worst
    strike = spot * math.exp(k_target)

    w1_val = svi_val(k_target, **p1)
    w2_val = svi_val(k_target, **p2_crossed)
    vol1 = math.sqrt(w1_val / t1)
    vol2 = math.sqrt(w2_val / t2)

    c1 = bs_call_price(spot, strike, rate, vol1, t1)
    c2 = bs_call_price(spot, strike, rate, vol2, t2)

    spread_cost = c2 - c1
    print(f"\nExecuting Calendar Spread (Buy T2={t2}, Sell T1={t1}) at Strike K = {strike:.2f}:")
    print(f"Near Call Price C(T1={t1}):  {c1:.4f} (Vol = {vol1:.4f})")
    print(f"Far Call Price C(T2={t2}):   {c2:.4f} (Vol = {vol2:.4f})")
    print(f"Net Calendar Spread Price:  {spread_cost:.4f}")
    print("Negative Cost for Longer Maturity Option (Arbitrage):", spread_cost < 0.0)


main()
