"""Lab 1 · Worked example: Arbitrage-Free Surface Builder on seed 0 (SIMULATED).

Executes the complete surface calibration pipeline on seed 0 instance parameters:
1. Loads simulated market option chains across expiries T in {0.25, 0.50, 0.75, 1.00}.
2. Calibrates raw SVI parameters per expiry slice via quasi-explicit optimization.
3. Certifies absence of butterfly arbitrage via Gatheral-Jacquier density factor g(k) >= 0.
4. Certifies absence of calendar arbitrage via total variance monotonicity w_{i+1}(k) >= w_i(k).
5. Extracts Dupire local volatility grid across strike and maturity dimensions.
"""

from __future__ import annotations

import math
from typing import Any


def svi_derivs(
    k: float, a: float, b: float, rho: float, m: float, sigma: float, **kwargs: Any
) -> tuple[float, float, float]:
    diff = k - m
    disc = math.sqrt(diff**2 + sigma**2)
    w = a + b * (rho * diff + disc)
    w_p = b * (rho + diff / disc)
    w_pp = b * (sigma**2) / (disc**3)
    return w, w_p, w_pp


def g_factor(k: float, a: float, b: float, rho: float, m: float, sigma: float, **kwargs: Any) -> float:
    w, w_p, w_pp = svi_derivs(k, a, b, rho, m, sigma)
    term1 = (1.0 - (k * w_p) / (2.0 * w)) ** 2
    term2 = (w_p**2 / 4.0) * (1.0 / w + 0.25)
    term3 = 0.5 * w_pp
    return term1 - term2 + term3


def fit_svi_slice(k_data: list[float], w_data: list[float]) -> dict[str, float]:
    n_obs = len(k_data)
    w_mean = sum(w_data) / n_obs

    def eval_3d(p: list[float]) -> tuple[float, float, float]:
        rho, m, sigma = p[0], p[1], p[2]
        if abs(rho) >= 0.99 or sigma <= 1e-4:
            return 1e6, 0.0, 0.0
        y = [rho * (k - m) + math.sqrt((k - m) ** 2 + sigma**2) for k in k_data]
        y_mean = sum(y) / n_obs
        var_y = sum((yi - y_mean) ** 2 for yi in y)
        if var_y < 1e-12:
            return 1e6, 0.0, 0.0
        cov_yw = sum((yi - y_mean) * (wi - w_mean) for yi, wi in zip(y, w_data, strict=True))
        b = max(0.0, cov_yw / var_y)
        b = min(b, 2.0 / (1.0 + abs(rho)))
        a = w_mean - b * y_mean
        min_w = a + b * sigma * math.sqrt(max(0.0, 1.0 - rho**2))
        if min_w < 0.0:
            a += -min_w
        err = sum((a + b * yi - wi) ** 2 for yi, wi in zip(y, w_data, strict=True))
        return err, a, b

    p0 = [-0.3, 0.0, 0.1]
    n = 3
    simplex = [list(p0)]
    for i in range(n):
        pt = list(p0)
        pt[i] += 0.05
        simplex.append(pt)

    for _ in range(200):
        simplex.sort(key=lambda p: eval_3d(p)[0])
        best = simplex[0]
        worst = simplex[-1]
        if eval_3d(worst)[0] - eval_3d(best)[0] < 1e-10:
            break
        centroid = [sum(simplex[j][i] for j in range(n)) / n for i in range(n)]
        refl = [centroid[i] + 1.0 * (centroid[i] - worst[i]) for i in range(n)]
        if eval_3d(simplex[0])[0] <= eval_3d(refl)[0] < eval_3d(simplex[-2])[0]:
            simplex[-1] = refl
            continue
        if eval_3d(refl)[0] < eval_3d(simplex[0])[0]:
            exp = [centroid[i] + 2.0 * (centroid[i] - worst[i]) for i in range(n)]
            simplex[-1] = exp if eval_3d(exp)[0] < eval_3d(refl)[0] else refl
            continue
        cont = [centroid[i] + 0.5 * (worst[i] - centroid[i]) for i in range(n)]
        if eval_3d(cont)[0] < eval_3d(worst)[0]:
            simplex[-1] = cont
            continue
        for j in range(1, n + 1):
            simplex[j] = [simplex[0][i] + 0.5 * (simplex[j][i] - simplex[0][i]) for i in range(n)]

    simplex.sort(key=lambda p: eval_3d(p)[0])
    best = simplex[0]
    err, a_opt, b_opt = eval_3d(best)
    return {
        "a": a_opt,
        "b": b_opt,
        "rho": best[0],
        "m": best[1],
        "sigma": best[2],
        "rmse": math.sqrt(err / n_obs),
    }


def main() -> None:
    # Seed 0 instance data (SIMULATED)
    spot = 115.33
    rate = 0.0453
    dividend = 0.0177
    expiries = [0.25, 0.50, 0.75, 1.00]
    forwards = [spot * math.exp((rate - dividend) * t) for t in expiries]

    # Benchmark parameter values for seed 0
    raw_params = [
        {"a": 0.01075, "b": 0.05500, "rho": -0.3241, "m": 0.005025, "sigma": 0.0500},
        {"a": 0.02150, "b": 0.08278, "rho": -0.3241, "m": 0.010050, "sigma": 0.0736},
        {"a": 0.03225, "b": 0.10526, "rho": -0.3241, "m": 0.015075, "sigma": 0.0929},
        {"a": 0.04300, "b": 0.12500, "rho": -0.3241, "m": 0.020100, "sigma": 0.1100},
    ]

    k_eval_grid = [-0.60, -0.40, -0.20, 0.00, 0.20, 0.40, 0.60]

    print("--- Seed 0 Surface Calibration Summary ---")
    print(f"Underlying Spot S0 = {spot:.2f} | Rate r = {rate:.4f} | Dividend q = {dividend:.4f}")
    print("Expiries (years):", expiries)

    calibrated_slices: list[dict[str, Any]] = []
    min_overall_g = float("inf")

    print("\n--- SVI Slice Calibration & Butterfly Arbitrage Checks ---")
    for i, t in enumerate(expiries):
        p = raw_params[i]
        # Generate simulated observations
        k_quotes = [-0.40, -0.25, -0.10, 0.0, 0.10, 0.25, 0.40]
        w_quotes = [svi_derivs(k, **p)[0] for k in k_quotes]

        fitted = fit_svi_slice(k_quotes, w_quotes)
        min_g = min(g_factor(k, **fitted) for k in k_eval_grid)
        if min_g < min_overall_g:
            min_overall_g = min_g

        calibrated_slices.append({"expiry": t, "forward": forwards[i], "params": fitted, "min_g": min_g})
        print(
            f"T = {t:.2f} | a={fitted['a']:.5f}, b={fitted['b']:.5f}, rho={fitted['rho']:.4f} | "
            f"Min g(k)={min_g:.5f} | Free: {min_g >= 0.0}"
        )

    print("\n--- Calendar Monotonicity Checks Across Consecutive Slices ---")
    min_cal_spread = float("inf")
    all_cal_free = True
    for i in range(len(calibrated_slices) - 1):
        s1 = calibrated_slices[i]
        s2 = calibrated_slices[i + 1]
        p1 = s1["params"]
        p2 = s2["params"]

        diffs = [svi_derivs(k, **p2)[0] - svi_derivs(k, **p1)[0] for k in k_eval_grid]
        min_d = min(diffs)
        if min_d < min_cal_spread:
            min_cal_spread = min_d
        if min_d < 0.0:
            all_cal_free = False
        print(f"Spread [T={s1['expiry']:.2f} -> T={s2['expiry']:.2f}]: Min dw = {min_d:.5f} | Free: {min_d >= 0.0}")

    print("\n--- Dupire Local Volatility Extraction at T = 0.25 ---")
    s1 = calibrated_slices[0]
    s2 = calibrated_slices[1]
    dt = s2["expiry"] - s1["expiry"]
    p_eval = s1["params"]

    print("Log-Moneyness (k) | Total Var w(k) | Density Factor g(k) | Local Vol sigma_loc(k)")
    print("-" * 80)
    for k in k_eval_grid:
        w1 = svi_derivs(k, **s1["params"])[0]
        w2 = svi_derivs(k, **s2["params"])[0]
        dw_dt = (w2 - w1) / dt
        g = g_factor(k, **p_eval)
        sigma_loc = math.sqrt(max(0.0, dw_dt / g))
        print(f"{k:17.2f} | {w1:16.5f} | {g:19.4f} | {sigma_loc:22.4f}")

    print("-" * 80)
    print("Butterfly Arbitrage-Free Certified:   ", min_overall_g >= 0.0)
    print("Calendar Arbitrage-Free Certified:    ", all_cal_free)
    print("Surface Fully Arbitrage-Free (PASS):  ", (min_overall_g >= 0.0) and all_cal_free)


main()
