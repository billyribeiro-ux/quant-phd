"""Lab 1 · Local Volatility: Dupire's Equation and Surface Extraction.

Extracts Dupire local volatility sigma_loc(k, tau) from total variance w(k, tau)
and Gatheral-Jacquier density factor g(k, tau). Verifies the rule of thumb that
local volatility skew is approximately twice the implied volatility skew at ATM.
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


def main() -> None:
    t1 = 0.40
    t2 = 0.60
    dt = t2 - t1
    t_mid = 0.50

    # Calibrated SVI parameters at t1 and t2 (SIMULATED)
    p1 = {"a": 0.024, "b": 0.100, "rho": -0.35, "m": 0.008, "sigma": 0.070}
    p2 = {"a": 0.036, "b": 0.125, "rho": -0.35, "m": 0.012, "sigma": 0.085}

    # Interpolated parameters at t_mid
    p_mid = {
        "a": 0.5 * (p1["a"] + p2["a"]),
        "b": 0.5 * (p1["b"] + p2["b"]),
        "rho": -0.35,
        "m": 0.5 * (p1["m"] + p2["m"]),
        "sigma": 0.5 * (p1["sigma"] + p2["sigma"]),
    }

    k_grid = [-0.40, -0.20, -0.10, 0.0, 0.10, 0.20, 0.40]

    print("Log-Moneyness (k) | Implied Vol (sigma_BS) | Local Vol (sigma_loc) | Density Factor g(k)")
    print("-" * 85)

    bs_vols: list[float] = []
    loc_vols: list[float] = []

    for k in k_grid:
        w1, _, _ = svi_derivs(k, **p1)
        w2, _, _ = svi_derivs(k, **p2)
        dw_dt = (w2 - w1) / dt

        g = g_factor(k, **p_mid)
        w_mid, _, _ = svi_derivs(k, **p_mid)
        sigma_bs = math.sqrt(w_mid / t_mid)

        loc_var = dw_dt / g
        sigma_loc = math.sqrt(max(0.0, loc_var))

        bs_vols.append(sigma_bs)
        loc_vols.append(sigma_loc)

        print(f"{k:17.2f} | {sigma_bs:22.4f} | {sigma_loc:21.4f} | {g:19.4f}")

    # Slope comparison around ATM (k in [-0.10, 0.10])
    idx_minus = k_grid.index(-0.10)
    idx_plus = k_grid.index(0.10)
    dk = k_grid[idx_plus] - k_grid[idx_minus]

    bs_skew = (bs_vols[idx_plus] - bs_vols[idx_minus]) / dk
    loc_skew = (loc_vols[idx_plus] - loc_vols[idx_minus]) / dk
    ratio = loc_skew / bs_skew if bs_skew != 0.0 else 0.0

    print("-" * 85)
    print(f"ATM Implied Volatility Skew (d sigma_BS / dk):  {bs_skew:.4f}")
    print(f"ATM Local Volatility Skew   (d sigma_loc / dk): {loc_skew:.4f}")
    print(f"Empirical Ratio (Local Skew / Implied Skew):     {ratio:.2f}")
    print("Dupire Smile Exaggeration Factor in [1.5, 2.5]:  ", 1.5 <= ratio <= 2.5)
    print("Local Volatility Exists & Positive Everywhere:  ", all(v > 0.0 for v in loc_vols))


main()
