"""Lab 2 · Averaging & Extremum Payoffs: Kemna-Vorst Asian Control Variates & Lookback Pricing.

Implements the Kemna & Vorst (1990) closed-form geometric Asian option pricer,
demonstrates its effectiveness as a high-precision control variate for arithmetic
Asian Monte Carlo simulation, and evaluates Goldman, Sosin & Gatto (1979)
continuous floating-strike lookbacks on seed 42 (SIMULATED).
"""

from __future__ import annotations

import math

import numpy as np


def norm_cdf(x: float) -> float:
    """Cumulative distribution function of standard normal distribution."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def geometric_asian_call_analytical(
    s0: float,
    k: float,
    t: float,
    r: float,
    q: float,
    sigma: float,
    n_obs: int,
) -> float:
    """Analytical Kemna & Vorst (1990) geometric Asian call price under discrete observation."""
    # Discrete observation times t_i = i * (T / n)
    mu = r - q - 0.5 * sigma * sigma
    mean_g = math.log(s0) + mu * t * (n_obs + 1.0) / (2.0 * n_obs)
    var_g = (sigma * sigma) * t * ((n_obs + 1.0) * (2.0 * n_obs + 1.0)) / (6.0 * n_obs * n_obs)
    std_g = math.sqrt(var_g)

    d2 = (mean_g - math.log(k)) / std_g
    d1 = d2 + std_g

    df = math.exp(-r * t)
    price = df * (math.exp(mean_g + 0.5 * var_g) * norm_cdf(d1) - k * norm_cdf(d2))
    return float(max(0.0, price))


def lookback_floating_call_analytical(
    s0: float,
    s_min: float,
    t: float,
    r: float,
    q: float,
    sigma: float,
) -> float:
    """Analytical Goldman, Sosin & Gatto (1979) floating-strike lookback call (S_T - S_min)."""
    if s_min > s0:
        raise ValueError("Minimum observed spot cannot exceed current spot")
    if t <= 0.0 or sigma <= 0.0:
        return max(0.0, s0 - s_min)

    b = r - q
    a1 = (math.log(s0 / s_min) + (b + 0.5 * sigma * sigma) * t) / (sigma * math.sqrt(t))
    a2 = a1 - sigma * math.sqrt(t)

    if abs(b) < 1e-7:
        # Limit as b -> 0
        term1 = s0 * norm_cdf(a1) - s_min * norm_cdf(a2)
        term2 = (
            s0
            * sigma
            * math.sqrt(t)
            * (norm_cdf(a1) * (a1) + (1.0 / math.sqrt(2.0 * math.pi)) * math.exp(-0.5 * a1 * a1))
        )
        return float(term1 + term2)

    power = -2.0 * b / (sigma * sigma)
    a3 = a1 + power * sigma * math.sqrt(t)

    term1 = s0 * math.exp(-q * t) * norm_cdf(a1)
    term2 = s_min * math.exp(-r * t) * norm_cdf(a2)
    term3 = (
        s0
        * math.exp(-r * t)
        * (sigma * sigma / (2.0 * b))
        * (math.exp(b * t) * norm_cdf(a1) - ((s0 / s_min) ** power) * norm_cdf(-a3))
    )
    return float(term1 - term2 + term3)


def simulate_asian_options(
    s0: float,
    k: float,
    t: float,
    r: float,
    q: float,
    sigma: float,
    n_obs: int,
    n_paths: int,
    seed: int = 42,
) -> dict[str, float]:
    """Monte Carlo simulation of arithmetic Asian with geometric control variate."""
    rng = np.random.default_rng(seed)
    dt = t / float(n_obs)
    sqrt_dt = math.sqrt(dt)
    drift = (r - q - 0.5 * sigma * sigma) * dt

    z = rng.standard_normal((n_paths, n_obs))
    log_increments = drift + sigma * sqrt_dt * z
    log_paths = np.empty((n_paths, n_obs + 1), dtype=np.float64)
    log_paths[:, 0] = math.log(s0)
    np.cumsum(log_increments, axis=1, out=log_paths[:, 1:])
    log_paths[:, 1:] += log_paths[:, 0:1]

    # Exclude t=0 from averaging (standard average of discrete fixings t_1 ... t_n)
    fixings = np.exp(log_paths[:, 1:])
    arithmetic_avg = np.mean(fixings, axis=1)
    geometric_avg = np.exp(np.mean(log_paths[:, 1:], axis=1))

    df = math.exp(-r * t)
    payoffs_arith = df * np.maximum(arithmetic_avg - k, 0.0)
    payoffs_geom = df * np.maximum(geometric_avg - k, 0.0)

    # Standard crude Monte Carlo
    price_arith_crude = float(np.mean(payoffs_arith))
    var_crude = float(np.var(payoffs_arith, ddof=1))
    se_crude = math.sqrt(var_crude / n_paths)

    # Analytical geometric price
    exact_geom = geometric_asian_call_analytical(s0, k, t, r, q, sigma, n_obs)

    # Optimal control variate coefficient c* = Cov(X, Y) / Var(Y)
    cov_matrix = np.cov(payoffs_arith, payoffs_geom, ddof=1)
    cov_xy = cov_matrix[0, 1]
    var_y = cov_matrix[1, 1]
    c_star = cov_xy / var_y if var_y > 0.0 else 0.0

    # Controlled estimator
    payoffs_controlled = payoffs_arith - c_star * (payoffs_geom - exact_geom)
    price_arith_cv = float(np.mean(payoffs_controlled))
    var_cv = float(np.var(payoffs_controlled, ddof=1))
    se_cv = math.sqrt(var_cv / n_paths)
    var_reduction = (1.0 - var_cv / var_crude) * 100.0 if var_crude > 0.0 else 0.0

    return {
        "crude_price": price_arith_crude,
        "crude_se": se_crude,
        "cv_price": price_arith_cv,
        "cv_se": se_cv,
        "exact_geom": exact_geom,
        "c_star": float(c_star),
        "variance_reduction_pct": var_reduction,
    }


def main() -> None:
    spot = 100.0
    strike = 100.0
    maturity = 1.0
    rate = 0.05
    div_yield = 0.02
    vol = 0.20
    n_obs = 12  # Monthly fixings

    # 1. Asian option evaluation
    asian_res = simulate_asian_options(
        spot, strike, maturity, rate, div_yield, vol, n_obs=n_obs, n_paths=50000, seed=42
    )

    # 2. Lookback option evaluation
    lb_floating = lookback_floating_call_analytical(spot, spot, maturity, rate, div_yield, vol)

    print("=== Lab 2: Asian & Lookback Option Valuation ===")
    print(f"Exact Geometric Asian Call:        {asian_res['exact_geom']:.4f}")
    print(f"Arithmetic Asian (Crude MC):       {asian_res['crude_price']:.4f} (SE: {asian_res['crude_se']:.4f})")
    print(f"Arithmetic Asian (Control Variate):{asian_res['cv_price']:.4f} (SE: {asian_res['cv_se']:.4f})")
    print(f"Optimal CV Coefficient (c*):       {asian_res['c_star']:.4f}")
    print(f"Variance Reduction Achieved:       {asian_res['variance_reduction_pct']:.2f}%")
    print(f"Floating-Strike Lookback Call:     {lb_floating:.4f}")


main()
