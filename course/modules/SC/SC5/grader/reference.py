"""Reference solution for SC5 project: Lévy model calibration engine (levy_calibration.py).

Implements:
1. Analytical risk-neutral characteristic functions for Merton jump-diffusion and Variance Gamma models.
2. Option pricing via Carr-Madan (1999) damped Fourier transform and Merton series.
3. Robust Black-Scholes implied volatility solver with no-arbitrage boundary validation.
4. Nonlinear least-squares calibration of Lévy parameters against empirical/simulated option surfaces.
"""

from __future__ import annotations

import math
from collections.abc import Callable
from typing import Any

import numpy as np
import scipy.optimize as opt  # type: ignore[import-untyped]
import scipy.stats as stats  # type: ignore[import-untyped]


def _bs_call(spot: float, strike: float, tau: float, r: float, vol: float) -> float:
    """Standard analytical Black-Scholes call price."""
    if vol <= 0.0 or tau <= 0.0:
        return max(0.0, spot - strike * math.exp(-r * tau))
    d1 = (math.log(spot / strike) + (r + 0.5 * vol**2) * tau) / (vol * math.sqrt(tau))
    d2 = d1 - vol * math.sqrt(tau)
    return float(spot * stats.norm.cdf(d1) - strike * math.exp(-r * tau) * stats.norm.cdf(d2))


def merton_characteristic_function(
    u: complex | np.ndarray,
    t: float,
    spot: float,
    r: float,
    sigma: float,
    lam: float,
    mu_j: float,
    sigma_j: float,
) -> complex | np.ndarray:
    """Evaluate the risk-neutral characteristic function E[exp(i*u*ln(S_t))] under Merton's jump-diffusion model.

    S_t = S_0 * exp((r - 0.5*sigma^2 - lam*kappa)*t + sigma*B_t + sum_{k=1}^{N_t} Y_k)
    where kappa = E[exp(Y) - 1] = exp(mu_j + 0.5*sigma_j^2) - 1, and Y ~ Normal(mu_j, sigma_j^2).
    """
    if spot <= 0.0 or t <= 0.0 or sigma <= 0.0 or lam < 0.0 or sigma_j <= 0.0:
        raise ValueError("Invalid parameters for Merton jump-diffusion characteristic function")

    u_arr = np.asarray(u)
    kappa = math.exp(mu_j + 0.5 * sigma_j**2) - 1.0
    drift = r - 0.5 * sigma**2 - lam * kappa
    jump_part = lam * (np.exp(1j * u_arr * mu_j - 0.5 * (sigma_j**2) * (u_arr**2)) - 1.0)
    psi = 1j * u_arr * drift - 0.5 * (sigma**2) * (u_arr**2) + jump_part
    cf = np.exp(1j * u_arr * math.log(spot)) * np.exp(t * psi)

    if isinstance(u, (complex, float, int)):
        return complex(cf.item())
    return cf


def vg_characteristic_function(
    u: complex | np.ndarray,
    t: float,
    spot: float,
    r: float,
    sigma: float,
    nu: float,
    theta: float,
) -> complex | np.ndarray:
    """Evaluate the risk-neutral characteristic function E[exp(i*u*ln(S_t))] under the Variance Gamma model.

    X_t = theta * G_t + sigma * B(G_t), G_t ~ Gamma(t/nu, nu).
    Martingale condition requires omega = (1/nu) * ln(1 - theta*nu - 0.5*sigma^2*nu),
    with admissibility condition 1 - theta*nu - 0.5*sigma^2*nu > 0.
    """
    if spot <= 0.0 or t <= 0.0 or sigma <= 0.0 or nu <= 0.0:
        raise ValueError("Parameters spot, t, sigma, and nu must be strictly positive")

    arg = 1.0 - theta * nu - 0.5 * (sigma**2) * nu
    if arg <= 0.0:
        raise ValueError(f"Variance Gamma admissibility condition violated: 1 - theta*nu - 0.5*sigma^2*nu = {arg} <= 0")

    u_arr = np.asarray(u)
    omega = (1.0 / nu) * math.log(arg)
    drift = (r + omega) * t
    denom = 1.0 - 1j * u_arr * theta * nu + 0.5 * (sigma**2) * nu * (u_arr**2)
    cf = np.exp(1j * u_arr * math.log(spot)) * np.exp(1j * u_arr * drift) * (denom ** (-t / nu))

    if isinstance(u, (complex, float, int)):
        return complex(cf.item())
    return cf


def _carr_madan_single_price(
    spot: float,
    strike: float,
    tau: float,
    r: float,
    cf_func: Callable[[complex | np.ndarray], complex | np.ndarray],
    alpha: float = 1.5,
    n_pts: int = 256,
    v_max: float = 100.0,
) -> float:
    """Carr-Madan (1999) damped Fourier inversion call pricer for a single strike."""
    k = math.log(strike)
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
    exp_term = np.exp(-1j * v * k)
    integrand = (exp_term * psi).real
    integral = float(np.sum(integrand * weights))
    call_price = float(math.exp(-alpha * k) / math.pi * integral)
    return max(0.0, call_price)


def _carr_madan_vector_prices(
    spot: float,
    strikes: np.ndarray,
    tau: float,
    r: float,
    cf_func: Callable[[complex | np.ndarray], complex | np.ndarray],
    alpha: float = 1.5,
    n_pts: int = 256,
    v_max: float = 100.0,
) -> np.ndarray:
    """Vectorized Carr-Madan (1999) pricer across an array of strikes."""
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
    call_prices = np.exp(-alpha * k) / math.pi * integral
    res: np.ndarray = np.asarray(np.maximum(0.0, call_prices), dtype=float)
    return res


def price_european_option(
    spot: float,
    strike: float,
    tenor: float,
    r: float,
    model: str,
    params: dict[str, float],
    is_call: bool = True,
) -> float:
    """Price a European option using Fourier inversion under the specified Lévy model ('merton' or 'vg')."""
    if spot <= 0.0 or strike <= 0.0 or tenor <= 0.0:
        raise ValueError("Spot, strike, and tenor must be strictly positive")

    model_key = model.lower().strip()
    if model_key in ("merton", "mjd"):

        def cf_merton(u: complex | np.ndarray) -> complex | np.ndarray:
            return merton_characteristic_function(
                u,
                tenor,
                spot,
                r,
                params["sigma"],
                params["lam"],
                params["mu_j"],
                params["sigma_j"],
            )

        call_price = _carr_madan_single_price(spot, strike, tenor, r, cf_merton)
    elif model_key in ("vg", "variance_gamma", "variance-gamma"):

        def cf_vg(u: complex | np.ndarray) -> complex | np.ndarray:
            return vg_characteristic_function(
                u,
                tenor,
                spot,
                r,
                params["sigma"],
                params["nu"],
                params["theta"],
            )

        call_price = _carr_madan_single_price(spot, strike, tenor, r, cf_vg)
    else:
        raise ValueError(f"Unknown Lévy model: {model!r}. Must be 'merton' or 'vg'.")

    if is_call:
        return call_price
    # Put-call parity: P = C - S_0 + K * exp(-r * tau)
    return float(call_price - spot + strike * math.exp(-r * tenor))


def implied_volatility(
    price: float,
    spot: float,
    strike: float,
    tenor: float,
    r: float,
    is_call: bool = True,
) -> float:
    """Invert Black-Scholes formula to recover implied volatility from European option price."""
    if spot <= 0.0 or strike <= 0.0 or tenor <= 0.0:
        raise ValueError("Spot, strike, and tenor must be positive")

    discount = math.exp(-r * tenor)
    intrinsic = max(0.0, spot - strike * discount) if is_call else max(0.0, strike * discount - spot)
    upper_bound = spot if is_call else strike * discount

    if price <= intrinsic or price >= upper_bound:
        raise ValueError(f"Option price {price} violates no-arbitrage bounds [{intrinsic:.4f}, {upper_bound:.4f}]")

    def obj(v: float) -> float:
        c = _bs_call(spot, strike, tenor, r, v)
        p = c if is_call else c - spot + strike * discount
        return p - price

    try:
        return float(opt.brentq(obj, 1e-4, 5.0, xtol=1e-7))
    except Exception as exc:
        raise ValueError(f"Implied volatility solver failed to converge: {exc}") from exc


def calibrate_model(
    market_surface: list[dict[str, Any]],
    model: str,
    spot: float,
    r: float,
    initial_guess: dict[str, float] | None = None,
) -> dict[str, Any]:
    """Calibrate model parameters ('merton' or 'vg') to market option surface via nonlinear least-squares."""
    if not market_surface:
        raise ValueError("Market surface cannot be empty")

    model_key = model.lower().strip()
    tenors = sorted(list({d["tenor"] for d in market_surface}))
    strikes_by_tenor = {
        tau: np.array([d["strike"] for d in market_surface if d["tenor"] == tau], dtype=float) for tau in tenors
    }
    prices_by_tenor = {
        tau: np.array([d["price"] for d in market_surface if d["tenor"] == tau], dtype=float) for tau in tenors
    }
    n_obs = len(market_surface)

    if model_key in ("merton", "mjd"):
        x0 = [0.15, 0.5, -0.10, 0.12]
        if initial_guess is not None:
            x0 = [
                initial_guess.get("sigma", 0.15),
                initial_guess.get("lam", 0.5),
                initial_guess.get("mu_j", -0.10),
                initial_guess.get("sigma_j", 0.12),
            ]
        bounds = ([0.05, 0.05, -0.40, 0.02], [0.45, 2.50, 0.10, 0.40])

        def residuals_merton(p: np.ndarray) -> np.ndarray:
            sigma, lam, mu_j, sigma_j = p
            res: list[float] = []
            for tau in tenors:

                def cf_at_tau(u: complex | np.ndarray, t_val: float = tau) -> complex | np.ndarray:
                    return merton_characteristic_function(u, t_val, spot, r, sigma, lam, mu_j, sigma_j)

                model_p = _carr_madan_vector_prices(spot, strikes_by_tenor[tau], tau, r, cf_at_tau)
                diff = model_p - prices_by_tenor[tau]
                res.extend(diff.tolist())
            return np.array(res, dtype=float)

        sol = opt.least_squares(residuals_merton, x0, bounds=bounds, ftol=1e-5, xtol=1e-5)
        rmse = float(math.sqrt(2.0 * sol.cost / n_obs))
        return {
            "params": {
                "sigma": float(sol.x[0]),
                "lam": float(sol.x[1]),
                "mu_j": float(sol.x[2]),
                "sigma_j": float(sol.x[3]),
            },
            "rmse": rmse,
            "status": str(sol.message),
        }

    if model_key in ("vg", "variance_gamma", "variance-gamma"):
        x0 = [0.20, 0.25, -0.12]
        if initial_guess is not None:
            x0 = [
                initial_guess.get("sigma", 0.20),
                initial_guess.get("nu", 0.25),
                initial_guess.get("theta", -0.12),
            ]
        bounds = ([0.05, 0.02, -0.45], [0.45, 0.80, 0.10])

        def residuals_vg(p: np.ndarray) -> np.ndarray:
            sigma, nu, theta = p
            arg = 1.0 - theta * nu - 0.5 * (sigma**2) * nu
            if arg <= 1e-4:
                return np.full(n_obs, 1e2)
            res: list[float] = []
            for tau in tenors:

                def cf_vg_at_tau(u: complex | np.ndarray, t_val: float = tau) -> complex | np.ndarray:
                    return vg_characteristic_function(u, t_val, spot, r, sigma, nu, theta)

                model_p = _carr_madan_vector_prices(spot, strikes_by_tenor[tau], tau, r, cf_vg_at_tau)
                diff = model_p - prices_by_tenor[tau]
                res.extend(diff.tolist())
            return np.array(res, dtype=float)

        sol = opt.least_squares(residuals_vg, x0, bounds=bounds, ftol=1e-5, xtol=1e-5)
        rmse = float(math.sqrt(2.0 * sol.cost / n_obs))
        return {
            "params": {
                "sigma": float(sol.x[0]),
                "nu": float(sol.x[1]),
                "theta": float(sol.x[2]),
            },
            "rmse": rmse,
            "status": str(sol.message),
        }

    raise ValueError(f"Unknown Lévy model: {model!r}. Must be 'merton' or 'vg'.")
