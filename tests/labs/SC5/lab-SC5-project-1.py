"""Rung 1 worked example: calibrating Merton jump-diffusion on seed 0 instance.

Demonstrates calibration of Merton's (1976) jump-diffusion model on the seed 0 SIMULATED option surface.
Evaluates the Carr-Madan (1999) damped Fourier transform pricer, sets up the nonlinear least-squares residual
vector across strikes and tenors, optimizes parameters (sigma, lambda, mu_j, sigma_j) using SciPy least_squares,
and verifies that the calibration achieves RMSE below 1e-3 on simulated quotes.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import scipy.optimize as opt  # type: ignore[import-untyped]


def merton_cf(
    u: complex | np.ndarray,
    tau: float,
    spot: float,
    r: float,
    sigma: float,
    lam: float,
    mu_j: float,
    sigma_j: float,
) -> complex | np.ndarray:
    kappa = math.exp(mu_j + 0.5 * sigma_j**2) - 1.0
    drift = r - 0.5 * sigma**2 - lam * kappa
    jump_part = lam * (np.exp(1j * u * mu_j - 0.5 * (sigma_j**2) * (u**2)) - 1.0)
    psi = 1j * u * drift - 0.5 * (sigma**2) * (u**2) + jump_part
    return np.exp(1j * u * math.log(spot)) * np.exp(tau * psi)


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
    true_merton = {"sigma": 0.123, "lam": 0.438, "mu_j": -0.128, "sigma_j": 0.159}

    tenors = [0.25, 0.50]
    strikes = np.array([90.0, 95.0, 100.0, 105.0, 110.0])

    # Construct synthetic market surface quotes from true parameters
    market_data: list[dict[str, Any]] = []
    for tau in tenors:

        def cf_at_tau(u: complex | np.ndarray, t_val: float = tau) -> complex | np.ndarray:
            return merton_cf(
                u,
                t_val,
                spot,
                r,
                true_merton["sigma"],
                true_merton["lam"],
                true_merton["mu_j"],
                true_merton["sigma_j"],
            )

        p_vec = carr_madan_vector_prices(spot, strikes, tau, r, cf_at_tau)
        for k, p in zip(strikes, p_vec, strict=True):
            market_data.append({"tenor": tau, "strike": k, "price": float(p)})

    # Calibration via nonlinear least-squares
    strikes_by_tenor = {
        tau: np.array([d["strike"] for d in market_data if d["tenor"] == tau], dtype=float) for tau in tenors
    }
    prices_by_tenor = {
        tau: np.array([d["price"] for d in market_data if d["tenor"] == tau], dtype=float) for tau in tenors
    }

    def residuals(params: np.ndarray) -> np.ndarray:
        sigma, lam, mu_j, sigma_j = params
        res: list[float] = []
        for tau in tenors:

            def cf_model(u: complex | np.ndarray, t_val: float = tau) -> complex | np.ndarray:
                return merton_cf(u, t_val, spot, r, sigma, lam, mu_j, sigma_j)

            model_p = carr_madan_vector_prices(spot, strikes_by_tenor[tau], tau, r, cf_model)
            diff = model_p - prices_by_tenor[tau]
            res.extend(diff.tolist())
        return np.array(res, dtype=float)

    init_guess = [0.15, 0.50, -0.10, 0.12]
    bounds = ([0.05, 0.05, -0.40, 0.02], [0.45, 2.50, 0.10, 0.40])
    sol = opt.least_squares(residuals, init_guess, bounds=bounds, ftol=1e-6, xtol=1e-6)

    calib_sigma, calib_lam, calib_mu_j, calib_sigma_j = sol.x
    rmse = math.sqrt(2.0 * sol.cost / len(market_data))

    print("seed 0 Merton jump-diffusion calibration (SIMULATED):")
    p_true_str = (
        f"sigma={true_merton['sigma']:.3f}, lambda={true_merton['lam']:.3f}, "
        f"mu_j={true_merton['mu_j']:.3f}, sigma_j={true_merton['sigma_j']:.3f}"
    )
    p_calib_str = f"sigma={calib_sigma:.3f}, lambda={calib_lam:.3f}, mu_j={calib_mu_j:.3f}, sigma_j={calib_sigma_j:.3f}"
    print(f"  true parameters:       {p_true_str}")
    print(f"  calibrated parameters: {p_calib_str}")
    print(f"  calibration RMSE: {rmse:.2e}")
    print("calibration converges with RMSE < 1e-3:", rmse < 1e-3)


main()
