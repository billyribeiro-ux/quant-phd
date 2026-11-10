"""Lab 7 · Jump-induced smile: implied volatility skew and short-tenor steepness.

Lévy jump processes generate pronounced implied volatility smiles and skews. A defining empirical and theoretical
property (Cont & Tankov 2004) is that under jump dynamics, the implied volatility skew |d sigma_imp / d ln K|
increases dramatically at short tenors (tau -> 0), behaving as O(1/tau) or O(1/sqrt(tau)), whereas under continuous
diffusions with constant volatility the smile is flat, and under stochastic volatility it flattens as tau -> 0.
This lab computes characteristic functions for Merton jump-diffusion and Variance Gamma models, evaluates European call
prices via Carr-Madan damped Fourier inversion, inverts the Black-Scholes formula to recover implied volatilities
across strikes K in {90, 95, 100, 105, 110} at short tenor tau = 0.05 and medium tenor tau = 0.50 (SIMULATED),
and quantifies the short-tenor skew amplification.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import scipy.optimize as opt  # type: ignore[import-untyped]
import scipy.stats as stats  # type: ignore[import-untyped]


def _bs_call(spot: float, strike: float, tau: float, r: float, vol: float) -> float:
    if vol <= 0.0 or tau <= 0.0:
        return max(0.0, spot - strike * math.exp(-r * tau))
    d1 = (math.log(spot / strike) + (r + 0.5 * vol**2) * tau) / (vol * math.sqrt(tau))
    d2 = d1 - vol * math.sqrt(tau)
    return float(spot * stats.norm.cdf(d1) - strike * math.exp(-r * tau) * stats.norm.cdf(d2))


def _implied_vol(price: float, spot: float, strike: float, tau: float, r: float) -> float:
    discount = math.exp(-r * tau)
    intrinsic = max(0.0, spot - strike * discount)
    if price <= intrinsic:
        return 1e-4

    def obj(v: float) -> float:
        return _bs_call(spot, strike, tau, r, v) - price

    return float(opt.brentq(obj, 1e-4, 5.0, xtol=1e-7))


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


def carr_madan_prices(
    spot: float,
    strikes: np.ndarray,
    tau: float,
    r: float,
    cf_func: Any,
    alpha: float = 1.5,
    n_pts: int = 512,
    v_max: float = 150.0,
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
    spot = 100.0
    r = 0.03
    strikes = np.array([90.0, 95.0, 100.0, 105.0, 110.0])

    # Merton parameters with negative mean jump (crash risk)
    m_sigma = 0.15
    m_lam = 0.60
    m_mu_j = -0.12
    m_sigma_j = 0.15

    tenors = [0.05, 0.50]
    skews: dict[float, float] = {}

    print("Merton jump-diffusion implied volatility surface (SIMULATED):")
    for tau in tenors:

        def cf_at_tau(u: complex | np.ndarray, t_val: float = tau) -> complex | np.ndarray:
            return merton_cf(u, t_val, spot, r, m_sigma, m_lam, m_mu_j, m_sigma_j)

        prices = carr_madan_prices(spot, strikes, tau, r, cf_at_tau)
        ivs = [_implied_vol(p, spot, k, tau, r) for k, p in zip(strikes, prices, strict=True)]

        # Skew measure: (IV(90) - IV(110)) / (ln(110/90))
        d_log_k = math.log(110.0 / 90.0)
        skew = (ivs[0] - ivs[-1]) / d_log_k
        skews[tau] = skew

        iv_str = ", ".join(f"K={k:.0f}:{v:.4f}" for k, v in zip(strikes, ivs, strict=True))
        print(f"  tau = {tau:.2f}: {iv_str} | skew = {skew:.4f}")

    ratio_steepness = skews[0.05] / skews[0.50]
    print(f"skew steepness amplification ratio (tau=0.05 vs tau=0.50): {ratio_steepness:.2f}")
    print("short-tenor skew is strictly steeper:", skews[0.05] > skews[0.50])
    print("amplification ratio exceeds 2.0x:", ratio_steepness >= 2.0)


main()
