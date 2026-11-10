"""Lab X2-L05-1: Global FX Volatility Innovation Factor & Cross-Sectional Pricing.

Implements the Menkhoff et al. (2012) global foreign exchange volatility proxy,
AR(1) innovation series, portfolio beta estimation, and Fama-MacBeth risk price tests.
"""

from __future__ import annotations

import random
from typing import Any


def simulate_volatility_pricing(
    n_months: int = 120,
    seed: int = 777,
) -> dict[str, Any]:
    """Simulate carry portfolios, global FX volatility innovations, and pricing tests.

    Args:
        n_months: Number of months.
        seed: Random seed.

    Returns:
        Dictionary of volatility betas, Fama-MacBeth lambda estimates, and R-squared.
    """
    rng = random.Random(seed)
    n_portfolios = 5

    # Simulate monthly global FX volatility as AR(1) process
    # Vol_t = c + rho * Vol_{t-1} + u_t
    c_vol = 0.002
    rho_vol = 0.65
    vol_series: list[float] = [0.008]
    innovations: list[float] = []

    for _ in range(n_months):
        u = rng.gauss(0.0, 0.002)
        v_next = c_vol + rho_vol * vol_series[-1] + u
        v_next = max(0.002, v_next)
        vol_series.append(v_next)
        innovations.append(u)

    # Monthly dollar factor
    dol_series = [rng.gauss(0.0, 0.02) for _ in range(n_months)]

    # Simulate 5 carry portfolios:
    # High carry portfolios have negative sensitivity to volatility shocks
    portfolio_returns: list[list[float]] = []
    # Volatility betas: P1 is positive (safe haven), P5 is negative (crash prone)
    true_vol_betas = [0.8, 0.3, -0.1, -0.6, -1.2]

    for t in range(n_months):
        u_t = innovations[t]
        dol_t = dol_series[t]
        month_row: list[float] = []
        for k in range(n_portfolios):
            # Base carry spread: -3% for P1 to +5% for P5
            base_yield = (-0.03 + k * 0.02) / 12.0
            ret = base_yield + 1.0 * dol_t + true_vol_betas[k] * u_t + rng.gauss(0.0, 0.005)
            month_row.append(ret)
        portfolio_returns.append(month_row)

    # Pass 1: Time-series regressions of each portfolio on [1, DOL, VOL_INNOV]
    betas_dol: list[float] = []
    betas_vol: list[float] = []
    mean_excess_returns: list[float] = []

    for k in range(n_portfolios):
        y = [portfolio_returns[t][k] for t in range(n_months)]
        x1 = dol_series
        x2 = innovations

        my = sum(y) / n_months
        m1 = sum(x1) / n_months
        m2 = sum(x2) / n_months

        s11 = sum((x - m1) ** 2 for x in x1)
        s22 = sum((x - m2) ** 2 for x in x2)
        s12 = sum((x1[t] - m1) * (x2[t] - m2) for t in range(n_months))
        sy1 = sum((y[t] - my) * (x1[t] - m1) for t in range(n_months))
        sy2 = sum((y[t] - my) * (x2[t] - m2) for t in range(n_months))

        det = s11 * s22 - s12 * s12
        b1 = (s22 * sy1 - s12 * sy2) / det
        b2 = (s11 * sy2 - s12 * sy1) / det

        betas_dol.append(round(b1, 3))
        betas_vol.append(round(b2, 3))
        mean_excess_returns.append(my)

    # Pass 2: Cross-sectional regression of mean excess returns on betas:
    # bar{R}_k = lambda_DOL * beta_{k, DOL} + lambda_VOL * beta_{k, VOL}
    # Solve 2x2 normal equations: (B'B) lambda = B' bar{R}
    b11 = sum(b1**2 for b1 in betas_dol)
    b22 = sum(b2**2 for b2 in betas_vol)
    b12 = sum(b1 * b2 for b1, b2 in zip(betas_dol, betas_vol, strict=True))

    br1 = sum(b1 * r for b1, r in zip(betas_dol, mean_excess_returns, strict=True))
    br2 = sum(b2 * r for b2, r in zip(betas_vol, mean_excess_returns, strict=True))

    det_b = b11 * b22 - b12 * b12
    lam_dol = (b22 * br1 - b12 * br2) / det_b
    lam_vol = (b11 * br2 - b12 * br1) / det_b

    fitted_means = [lam_dol * b1 + lam_vol * b2 for b1, b2 in zip(betas_dol, betas_vol, strict=True)]
    ss_tot = sum((r - (sum(mean_excess_returns) / n_portfolios)) ** 2 for r in mean_excess_returns)
    ss_res = sum((r - f) ** 2 for r, f in zip(mean_excess_returns, fitted_means, strict=True))
    cs_r2 = 1.0 - (ss_res / ss_tot)

    return {
        "n_months": n_months,
        "betas_dol": betas_dol,
        "betas_vol": betas_vol,
        "mean_excess_returns_ann": [round(r * 12.0 * 100, 2) for r in mean_excess_returns],
        "lambda_dol_ann": round(lam_dol * 12.0 * 100, 2),
        "lambda_vol_monthly": round(lam_vol, 5),
        "cross_sectional_r2": round(cs_r2, 3),
    }


def main() -> None:
    res = simulate_volatility_pricing(n_months=120, seed=777)
    print("=== Global FX Volatility Risk Pricing (Menkhoff et al. 2012) ===")
    print(f"Sample: {res['n_months']} months")
    print("Port | Mean Return | Beta (DOL) | Beta (Vol) ")
    print("---------------------------------------------")
    for k in range(5):
        ret_s = f"{res['mean_excess_returns_ann'][k]:>9.2f}%"
        b_dol = f"{res['betas_dol'][k]:>10.3f}"
        b_vol = f"{res['betas_vol'][k]:>10.3f}"
        print(f"P{k + 1:<4}| {ret_s} | {b_dol} | {b_vol}")
    print("---------------------------------------------")
    print(f"Cross-Sectional R^2: {res['cross_sectional_r2']:.3f}")
    print(f"Price of Volatility Risk lambda_VOL: {res['lambda_vol_monthly']} (negative, compensation for vol risk)")


main()
