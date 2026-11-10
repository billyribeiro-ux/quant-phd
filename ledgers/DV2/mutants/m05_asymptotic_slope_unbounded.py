"""Student error: allows negative wing slope parameter b by disabling non-negativity check."""

from __future__ import annotations

import math
from typing import Any


def svi_total_variance(k: float, a: float, b: float, rho: float, m: float, sigma: float) -> float:
    # Student error: omits non-negativity validation for b (allowing negative b)
    if abs(rho) >= 1.0:
        raise ValueError(f"SVI parameter rho must satisfy |rho| < 1, got {rho}")
    if sigma <= 0.0:
        raise ValueError(f"SVI parameter sigma must be strictly positive, got {sigma}")

    min_w = a + b * sigma * math.sqrt(max(0.0, 1.0 - rho**2))
    if min_w < -1e-12:
        raise ValueError(f"SVI minimum total variance must be non-negative, got {min_w}")

    diff = k - m
    disc = math.sqrt(diff**2 + sigma**2)
    return float(a + b * (rho * diff + disc))


def svi_derivatives(k: float, a: float, b: float, rho: float, m: float, sigma: float) -> tuple[float, float, float]:
    w = svi_total_variance(k, a, b, rho, m, sigma)
    diff = k - m
    disc = math.sqrt(diff**2 + sigma**2)
    w_p = b * (rho + diff / disc)
    w_pp = b * (sigma**2) / (disc**3)
    return w, w_p, w_pp


def svi_density_factor(k: float, a: float, b: float, rho: float, m: float, sigma: float) -> float:
    w, w_p, w_pp = svi_derivatives(k, a, b, rho, m, sigma)
    if w <= 1e-12:
        raise ValueError("Total variance w(k) must be strictly positive to compute density factor")

    term1 = (1.0 - (k * w_p) / (2.0 * w)) ** 2
    term2 = (w_p**2 / 4.0) * (1.0 / w + 0.25)
    term3 = 0.5 * w_pp
    return term1 - term2 + term3


def check_butterfly_arbitrage(k_grid: list[float], params: dict[str, float]) -> tuple[bool, float]:
    if not k_grid:
        raise ValueError("k_grid must not be empty")

    a = params["a"]
    b = params["b"]
    rho = params["rho"]
    m = params["m"]
    sigma = params["sigma"]

    min_g = float("inf")
    for k in k_grid:
        g = svi_density_factor(k, a, b, rho, m, sigma)
        if g < min_g:
            min_g = g

    return (min_g >= 0.0, min_g)


def check_calendar_arbitrage(
    k_grid: list[float],
    t1: float,
    params1: dict[str, float],
    t2: float,
    params2: dict[str, float],
) -> tuple[bool, float]:
    if t1 <= 0.0 or t2 <= 0.0:
        raise ValueError(f"Expirations must be strictly positive: t1={t1}, t2={t2}")
    if t2 <= t1:
        raise ValueError(f"t2 must be strictly greater than t1: t1={t1}, t2={t2}")
    if not k_grid:
        raise ValueError("k_grid must not be empty")

    a1, b1, rho1, m1, sigma1 = (
        params1["a"],
        params1["b"],
        params1["rho"],
        params1["m"],
        params1["sigma"],
    )
    a2, b2, rho2, m2, sigma2 = (
        params2["a"],
        params2["b"],
        params2["rho"],
        params2["m"],
        params2["sigma"],
    )

    min_diff = float("inf")
    for k in k_grid:
        w1 = svi_total_variance(k, a1, b1, rho1, m1, sigma1)
        w2 = svi_total_variance(k, a2, b2, rho2, m2, sigma2)
        diff = w2 - w1
        if diff < min_diff:
            min_diff = diff

    return (min_diff >= 0.0, min_diff)


def fit_svi_slice(
    k_data: list[float],
    w_data: list[float],
    init_guess: dict[str, float] | None = None,
) -> dict[str, float]:
    n_obs = len(k_data)
    if n_obs != len(w_data) or n_obs < 5:
        raise ValueError(f"Expected at least 5 observations with matching lengths, got {n_obs} vs {len(w_data)}")
    for w in w_data:
        if w <= 0.0:
            raise ValueError(f"Observed total variance must be strictly positive, got {w}")

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
        cov_yw = sum((yi - y_mean) * (wi - w_mean) for yi, wi in zip(y, w_data, strict=False))
        b = max(0.0, cov_yw / var_y)
        b = min(b, 2.0 / (1.0 + abs(rho)))
        a = w_mean - b * y_mean
        min_w = a + b * sigma * math.sqrt(max(0.0, 1.0 - rho**2))
        if min_w < 0.0:
            a += -min_w
        err = sum((a + b * yi - wi) ** 2 for yi, wi in zip(y, w_data, strict=False))
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
    rmse = math.sqrt(err / n_obs)

    return {
        "a": a_opt,
        "b": b_opt,
        "rho": best[0],
        "m": best[1],
        "sigma": best[2],
        "rmse": rmse,
    }


def extract_local_volatility(k: float, t: float, slices: list[dict[str, Any]]) -> float:
    if len(slices) < 2:
        raise ValueError(f"Need at least 2 slices to extract local volatility, got {len(slices)}")

    sorted_slices = sorted(slices, key=lambda s: float(s["expiry"]))
    expiries = [float(s["expiry"]) for s in sorted_slices]

    if t < expiries[0] or t > expiries[-1]:
        raise ValueError(f"Maturity t={t} outside slice range [{expiries[0]}, {expiries[-1]}]")

    idx = 0
    for i in range(len(expiries) - 1):
        if expiries[i] <= t <= expiries[i + 1]:
            idx = i
            break

    t1, t2 = expiries[idx], expiries[idx + 1]
    p1, p2 = sorted_slices[idx]["params"], sorted_slices[idx + 1]["params"]

    w1 = svi_total_variance(k, p1["a"], p1["b"], p1["rho"], p1["m"], p1["sigma"])
    w2 = svi_total_variance(k, p2["a"], p2["b"], p2["rho"], p2["m"], p2["sigma"])

    dt = t2 - t1
    if dt <= 1e-12:
        raise ValueError("Slice maturities must be distinct")
    dw_dt = (w2 - w1) / dt

    alpha = (t - t1) / dt if dt > 0 else 0.0
    a_t = p1["a"] * (1.0 - alpha) + p2["a"] * alpha
    b_t = p1["b"] * (1.0 - alpha) + p2["b"] * alpha
    rho_t = p1["rho"] * (1.0 - alpha) + p2["rho"] * alpha
    m_t = p1["m"] * (1.0 - alpha) + p2["m"] * alpha
    sigma_t = p1["sigma"] * (1.0 - alpha) + p2["sigma"] * alpha

    g = svi_density_factor(k, a_t, b_t, rho_t, m_t, sigma_t)

    if dw_dt < 0.0:
        raise ValueError(f"Calendar arbitrage detected: dw/dt = {dw_dt} < 0")
    if g <= 0.0:
        raise ValueError(f"Butterfly arbitrage detected: density factor g = {g} <= 0")

    loc_var = dw_dt / g
    return math.sqrt(max(0.0, loc_var))


def build_arbitrage_free_surface(chain_data: list[dict[str, Any]], k_eval_grid: list[float]) -> dict[str, Any]:
    calibrated_slices: list[dict[str, Any]] = []
    min_density = float("inf")

    for item in chain_data:
        t = float(item["expiry"])
        fwd = float(item["forward"])
        quotes = item["quotes"]
        k_data = [float(q["log_moneyness"]) for q in quotes]
        w_data = [float(q["total_variance"]) for q in quotes]

        fitted = fit_svi_slice(k_data, w_data)
        is_free_bf, min_g = check_butterfly_arbitrage(k_eval_grid, fitted)
        if min_g < min_density:
            min_density = min_g

        calibrated_slices.append(
            {
                "expiry": t,
                "forward": fwd,
                "params": fitted,
                "butterfly_free": is_free_bf,
                "min_g": min_g,
            }
        )

    min_cal_spread = float("inf")
    calendar_free = True
    for i in range(len(calibrated_slices) - 1):
        s1 = calibrated_slices[i]
        s2 = calibrated_slices[i + 1]
        is_cal_free, min_diff = check_calendar_arbitrage(
            k_eval_grid,
            float(s1["expiry"]),
            s1["params"],
            float(s2["expiry"]),
            s2["params"],
        )
        if min_diff < min_cal_spread:
            min_cal_spread = min_diff
        if not is_cal_free:
            calendar_free = False

    local_vol_grid: list[list[float]] = []
    for s in calibrated_slices[:-1]:
        t_eval = float(s["expiry"])
        row: list[float] = []
        for k in k_eval_grid:
            vol_loc = extract_local_volatility(k, t_eval, calibrated_slices)
            row.append(vol_loc)
        local_vol_grid.append(row)

    is_surface_free = (min_density >= 0.0) and calendar_free

    return {
        "calibrated_slices": calibrated_slices,
        "is_arbitrage_free": is_surface_free,
        "min_density": min_density,
        "min_calendar_spread": min_cal_spread,
        "local_vol_grid": local_vol_grid,
    }
