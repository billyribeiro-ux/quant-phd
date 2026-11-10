"""Per-learner instances for the SC5 autograder of Lévy model calibration. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library and NumPy.
From the seed alone it draws:

* underlying asset state: spot = 100.0, risk-free rate r in [0.02, 0.05], dividend yield q = 0.0;
* Merton jump-diffusion parameters:
  - diffusion volatility m_sigma in [0.12, 0.22];
  - jump arrival intensity m_lam in [0.3, 0.8];
  - mean jump size m_mu_j in [-0.15, -0.05];
  - jump size standard deviation m_sigma_j in [0.10, 0.18];
* Variance Gamma parameters:
  - volatility vg_sigma in [0.15, 0.28];
  - variance rate vg_nu in [0.15, 0.35];
  - drift/skewness vg_theta in [-0.20, -0.05];
* grid of strikes [90.0, 95.0, 100.0, 105.0, 110.0] and tenors [0.25, 0.5];
* precomputed SIMULATED option price and implied volatility lists for Merton and Variance Gamma.

The instance carries the seed and the label "SIMULATED". Nothing here is a real market, a real price or a real asset.
"""

from __future__ import annotations

import math
import random
from typing import Any

import numpy as np


def _bs_call(spot: float, strike: float, tau: float, r: float, vol: float) -> float:
    """Analytical Black-Scholes call price."""
    if vol <= 0.0 or tau <= 0.0:
        return max(0.0, spot - strike * math.exp(-r * tau))
    d1 = (math.log(spot / strike) + (r + 0.5 * vol**2) * tau) / (vol * math.sqrt(tau))
    d2 = d1 - vol * math.sqrt(tau)
    cdf1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
    cdf2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
    return spot * cdf1 - strike * math.exp(-r * tau) * cdf2


def _implied_vol(price: float, spot: float, strike: float, tau: float, r: float) -> float:
    """Invert Black-Scholes formula using bisection with high precision."""
    intrinsic = max(0.0, spot - strike * math.exp(-r * tau))
    if price <= intrinsic:
        return 1e-4
    low, high = 1e-4, 4.0
    for _ in range(60):
        mid = 0.5 * (low + high)
        p_mid = _bs_call(spot, strike, tau, r, mid)
        if p_mid < price:
            low = mid
        else:
            high = mid
    return 0.5 * (low + high)


def _merton_series_call(
    spot: float, strike: float, tau: float, r: float, sigma: float, lam: float, mu_j: float, sigma_j: float
) -> float:
    """Merton (1976) series formula for European call option."""
    kappa = math.exp(mu_j + 0.5 * sigma_j**2) - 1.0
    price_sum = 0.0
    lam_tau = lam * tau
    drift_base = (r - 0.5 * sigma**2 - lam * kappa) * tau
    var_base = sigma**2 * tau
    p_n = math.exp(-lam_tau)
    log_sk = math.log(spot / strike)
    for n in range(50):
        if n > 0:
            p_n *= lam_tau / n
        m_n = drift_base + n * mu_j
        v_n = math.sqrt(var_base + n * sigma_j**2)
        d1 = (log_sk + m_n + v_n**2) / v_n
        d2 = d1 - v_n
        cdf1 = 0.5 * (1.0 + math.erf(d1 / math.sqrt(2.0)))
        cdf2 = 0.5 * (1.0 + math.erf(d2 / math.sqrt(2.0)))
        payoff = spot * math.exp(m_n + 0.5 * v_n**2) * cdf1 - strike * cdf2
        price_sum += p_n * payoff
        if p_n < 1e-13 and n > 5:
            break
    return price_sum * math.exp(-r * tau)


def _carr_madan_vg_prices(
    spot: float, strikes: list[float], tau: float, r: float, sigma: float, nu: float, theta: float
) -> list[float]:
    """Carr-Madan (1999) damped Fourier transform pricing for Variance Gamma."""
    alpha = 1.5
    n_pts = 256
    v_max = 100.0
    v = np.linspace(0.0, v_max, n_pts + 1)
    dv = v_max / n_pts
    weights = np.ones(n_pts + 1)
    weights[1:-1:2] = 4.0
    weights[2:-2:2] = 2.0
    weights = weights * (dv / 3.0)

    arg = 1.0 - theta * nu - 0.5 * (sigma**2) * nu
    omega = (1.0 / nu) * math.log(arg)
    drift = (r + omega) * tau

    u = v - (alpha + 1.0) * 1j
    denom_cf = 1.0 - 1j * u * theta * nu + 0.5 * (sigma**2) * nu * (u**2)
    phi = np.exp(1j * u * math.log(spot)) * np.exp(1j * u * drift) * (denom_cf ** (-tau / nu))

    denom = (alpha**2 + alpha - v**2) + 1j * (2.0 * alpha + 1.0) * v
    psi = np.exp(-r * tau) * phi / denom

    strikes_arr = np.asarray(strikes, dtype=float)
    k = np.log(strikes_arr)
    exp_term = np.exp(-1j * np.outer(k, v))
    integrand = (exp_term * psi).real
    integral = np.sum(integrand * weights, axis=1)
    prices = np.exp(-alpha * k) / math.pi * integral
    return [float(max(0.0, p)) for p in prices]


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic SIMULATED instance for ``seed``."""
    rng = random.Random(1_000_003 * int(seed) + 42)
    spot = 100.0
    r = round(rng.uniform(0.02, 0.05), 3)
    q = 0.0

    m_sigma = round(rng.uniform(0.12, 0.22), 3)
    m_lam = round(rng.uniform(0.3, 0.8), 3)
    m_mu_j = round(rng.uniform(-0.15, -0.05), 3)
    m_sigma_j = round(rng.uniform(0.10, 0.18), 3)

    vg_sigma = round(rng.uniform(0.15, 0.28), 3)
    vg_nu = round(rng.uniform(0.15, 0.35), 3)
    vg_theta = round(rng.uniform(-0.20, -0.05), 3)

    tenors = [0.25, 0.5]
    strikes = [90.0, 95.0, 100.0, 105.0, 110.0]

    merton_prices: list[float] = []
    merton_ivs: list[float] = []
    vg_prices: list[float] = []
    vg_ivs: list[float] = []

    for tau in tenors:
        for k in strikes:
            p_m = _merton_series_call(spot, k, tau, r, m_sigma, m_lam, m_mu_j, m_sigma_j)
            iv_m = _implied_vol(p_m, spot, k, tau, r)
            merton_prices.append(round(p_m, 6))
            merton_ivs.append(round(iv_m, 6))

        p_vg_list = _carr_madan_vg_prices(spot, strikes, tau, r, vg_sigma, vg_nu, vg_theta)
        for k, p_vg in zip(strikes, p_vg_list, strict=True):
            iv_vg = _implied_vol(p_vg, spot, k, tau, r)
            vg_prices.append(round(float(p_vg), 6))
            vg_ivs.append(round(iv_vg, 6))

    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "spot": spot,
        "r": r,
        "q": q,
        "m_sigma": m_sigma,
        "m_lam": m_lam,
        "m_mu_j": m_mu_j,
        "m_sigma_j": m_sigma_j,
        "vg_sigma": vg_sigma,
        "vg_nu": vg_nu,
        "vg_theta": vg_theta,
        "tenors": tenors,
        "strikes": strikes,
        "merton_prices": merton_prices,
        "merton_ivs": merton_ivs,
        "vg_prices": vg_prices,
        "vg_ivs": vg_ivs,
    }


def make_surface(instance: dict[str, Any], model: str) -> list[dict[str, Any]]:
    """Helper to reconstruct structured option quote dictionaries from the instance fields."""
    model_key = model.lower().strip()
    is_merton = model_key in ("merton", "mjd")
    prices: list[float] = instance["merton_prices"] if is_merton else instance["vg_prices"]
    ivs: list[float] = instance["merton_ivs"] if is_merton else instance["vg_ivs"]
    tenors: list[float] = instance["tenors"]
    strikes: list[float] = instance["strikes"]

    surface: list[dict[str, Any]] = []
    idx = 0
    for tau in tenors:
        for k in strikes:
            surface.append({
                "tenor": tau,
                "strike": k,
                "price": prices[idx],
                "implied_vol": ivs[idx],
                "is_call": True,
            })
            idx += 1
    return surface
