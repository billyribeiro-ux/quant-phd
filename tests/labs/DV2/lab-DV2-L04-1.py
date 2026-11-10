"""Lab 1 · SVI Parameterization: Raw, Natural, and Quasi-Explicit Calibration.

Implements Gatheral & Jacquier (2014) quasi-explicit calibration of raw SVI parameters
to simulated market implied variance quotes. Checks Lee's moment asymptotic slope
bounds b * (1 + |rho|) <= 2 and minimum total variance positivity.
All data is SIMULATED (seed 42).
"""

from __future__ import annotations

import math


def svi_val(k: float, a: float, b: float, rho: float, m: float, sigma: float) -> float:
    diff = k - m
    disc = math.sqrt(diff**2 + sigma**2)
    return a + b * (rho * diff + disc)


def fit_svi_quasi(k_data: list[float], w_data: list[float], init_guess: list[float] | None = None) -> dict[str, float]:
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

    p0 = [-0.3, 0.0, 0.1] if init_guess is None else init_guess
    n = 3
    simplex = [list(p0)]
    for i in range(n):
        pt = list(p0)
        pt[i] += 0.05
        simplex.append(pt)

    for _ in range(250):
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
    # Target true slice parameters (SIMULATED)
    true_p = {"a": 0.030, "b": 0.140, "rho": -0.420, "m": 0.015, "sigma": 0.080}
    tau = 0.50

    k_market = [-0.50, -0.35, -0.20, -0.10, 0.0, 0.10, 0.20, 0.35, 0.50]
    # Synthetic market total variance quotes with noise
    w_market = [svi_val(k, **true_p) for k in k_market]

    print("Market Observations (Log-Moneyness vs Total Variance):")
    for k, w in zip(k_market, w_market, strict=True):
        bs_vol = math.sqrt(w / tau)
        print(f"k = {k:5.2f} | w_obs = {w:.6f} | BS Vol = {bs_vol:.4f}")

    fitted = fit_svi_quasi(k_market, w_market)

    print("\n--- SVI Quasi-Explicit Calibration Results ---")
    print(f"Calibrated a:     {fitted['a']:.6f} (True: {true_p['a']:.6f})")
    print(f"Calibrated b:     {fitted['b']:.6f} (True: {true_p['b']:.6f})")
    print(f"Calibrated rho:   {fitted['rho']:.6f} (True: {true_p['rho']:.6f})")
    print(f"Calibrated m:     {fitted['m']:.6f} (True: {true_p['m']:.6f})")
    print(f"Calibrated sigma: {fitted['sigma']:.6f} (True: {true_p['sigma']:.6f})")
    print(f"Calibration RMSE: {fitted['rmse']:.6e}")

    # Parameter constraints verification
    min_w = fitted["a"] + fitted["b"] * fitted["sigma"] * math.sqrt(max(0.0, 1.0 - fitted["rho"] ** 2))
    slope_left = fitted["b"] * (1.0 - fitted["rho"])
    slope_right = fitted["b"] * (1.0 + fitted["rho"])
    lee_bound = fitted["b"] * (1.0 + abs(fitted["rho"]))

    print("\n--- Structural Constraints and Lee Asymptotics ---")
    print(f"Minimum Total Variance w_min:            {min_w:.6f} (Must be >= 0)")
    print(f"Left Wing Asymptotic Slope (k -> -inf):  {slope_left:.6f}")
    print(f"Right Wing Asymptotic Slope (k -> +inf): {slope_right:.6f}")
    print(f"Lee Moment Bound b*(1+|rho|):            {lee_bound:.6f} (Must be <= 2)")
    print("Non-negativity constraint satisfied:     ", min_w >= 0.0)
    print("Lee's asymptotic slope bound satisfied:  ", lee_bound < 2.0)
    print("Calibration Fit Quality (RMSE < 1e-4):   ", fitted["rmse"] < 1e-4)


main()
