"""Rung 2 completion problem: completing the Variance Gamma calibration engine.

Completes the Variance Gamma characteristic function pricing and calibration engine on seed 0 (SIMULATED).
Verifies the martingale drift correction omega = (1/nu)*ln(1 - theta*nu - 0.5*sigma^2*nu), calibrates
(sigma, nu, theta) to the simulated option surface, and checks that calibration RMSE is below 1e-3.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import scipy.optimize as opt  # type: ignore[import-untyped]


def vg_cf(
    u: complex | np.ndarray,
    tau: float,
    spot: float,
    r: float,
    sigma: float,
    nu: float,
    theta: float,
) -> complex | np.ndarray:
    arg = 1.0 - theta * nu - 0.5 * (sigma**2) * nu
    if arg <= 0.0:
        raise ValueError("VG admissibility condition violated")
    omega = (1.0 / nu) * math.log(arg)
    drift = (r + omega) * tau
    denom = 1.0 - 1j * u * theta * nu + 0.5 * (sigma**2) * nu * (u**2)
    return np.exp(1j * u * math.log(spot)) * np.exp(1j * u * drift) * (denom ** (-tau / nu))


def carr_madan_vector_prices(
    spot: float,
    strikes: np.ndarray,
    tau: float,
    r: float,
    cf_func: Any,
    alpha: float = 1.5,
    n_pts: int = 256,
    v_max: float = 100.0,
) -> np.ndarray:
    k = np.log(strikes)
    v = np.linspace(0.0, v_max, n_pts + 1)
    dv = v_max / n_pts
    weights = np.ones(n_pts + 1)
    weights[1:-1:2] = 4.0
    weights[2:-2:2] = 2.0
    weights = weights * (dv / 3.0)

    u = v - (alpha + 1.0) * 1j
    phi = cf_func(u)
    denom = (alpha**2 + alpha - v**2) + 1j * (2.0 * alpha + 1.0) * v
    psi = np.exp(-r * tau) * phi / denom
    exp_term = np.exp(-1j * np.outer(k, v))
    integrand = (exp_term * psi).real
    integral = np.sum(integrand * weights, axis=1)
    res: np.ndarray = np.asarray(np.maximum(0.0, np.exp(-alpha * k) / math.pi * integral), dtype=float)
    return res


def main() -> None:
    # Seed 0 parameters (SIMULATED)
    spot = 100.0
    r = 0.039
    true_vg = {"sigma": 0.238, "nu": 0.328, "theta": -0.187}

    tenors = [0.25, 0.50]
    strikes = np.array([90.0, 95.0, 100.0, 105.0, 110.0])

    market_data: list[dict[str, Any]] = []
    for tau in tenors:

        def cf_at_tau(u: complex | np.ndarray, t_val: float = tau) -> complex | np.ndarray:
            return vg_cf(
                u,
                t_val,
                spot,
                r,
                true_vg["sigma"],
                true_vg["nu"],
                true_vg["theta"],
            )

        p_vec = carr_madan_vector_prices(spot, strikes, tau, r, cf_at_tau)
        for k, p in zip(strikes, p_vec, strict=True):
            market_data.append({"tenor": tau, "strike": k, "price": float(p)})

    strikes_by_tenor = {
        tau: np.array([d["strike"] for d in market_data if d["tenor"] == tau], dtype=float) for tau in tenors
    }
    prices_by_tenor = {
        tau: np.array([d["price"] for d in market_data if d["tenor"] == tau], dtype=float) for tau in tenors
    }

    def residuals(params: np.ndarray) -> np.ndarray:
        sigma, nu, theta = params
        arg = 1.0 - theta * nu - 0.5 * (sigma**2) * nu
        if arg <= 1e-4:
            return np.full(len(market_data), 1e2)
        res: list[float] = []
        for tau in tenors:

            def cf_model(u: complex | np.ndarray, t_val: float = tau) -> complex | np.ndarray:
                return vg_cf(u, t_val, spot, r, sigma, nu, theta)

            model_p = carr_madan_vector_prices(spot, strikes_by_tenor[tau], tau, r, cf_model)
            diff = model_p - prices_by_tenor[tau]
            res.extend(diff.tolist())
        return np.array(res, dtype=float)

    init_guess = [0.20, 0.25, -0.12]
    bounds = ([0.05, 0.02, -0.45], [0.45, 0.80, 0.10])
    sol = opt.least_squares(residuals, init_guess, bounds=bounds, ftol=1e-6, xtol=1e-6)

    calib_sigma, calib_nu, calib_theta = sol.x
    rmse = math.sqrt(2.0 * sol.cost / len(market_data))

    print("seed 0 Variance Gamma calibration (SIMULATED):")
    p_true_str = f"sigma={true_vg['sigma']:.3f}, nu={true_vg['nu']:.3f}, theta={true_vg['theta']:.3f}"
    p_calib_str = f"sigma={calib_sigma:.3f}, nu={calib_nu:.3f}, theta={calib_theta:.3f}"
    print(f"  true parameters:       {p_true_str}")
    print(f"  calibrated parameters: {p_calib_str}")
    print(f"  calibration RMSE: {rmse:.2e}")
    print("calibration converges with RMSE < 1e-3:", rmse < 1e-3)


main()
