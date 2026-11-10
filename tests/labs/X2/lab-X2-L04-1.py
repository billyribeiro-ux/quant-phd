"""Lab X2-L04-1: Lustig-Roussanov-Verdelhan Dollar & HML-FX Decomposition.

Replicates cross-sectional currency portfolio sorting, Dollar level factor,
and HML-FX slope factor regressions (Lustig, Roussanov & Verdelhan 2011).
"""

from __future__ import annotations

import random
from typing import Any


def simulate_factor_decomposition(
    n_months: int = 120,
    seed: int = 42,
) -> dict[str, Any]:
    """Sort currencies into 5 quintiles and decompose into Level and Slope factors.

    Args:
        n_months: Sample length in months.
        seed: Random seed.

    Returns:
        Dictionary containing portfolio returns, factor returns, and regression results.
    """
    rng = random.Random(seed)
    n_portfolios = 5

    # Base interest differentials (funding vs target)

    portfolio_returns: list[list[float]] = []

    # Monthly common dollar factor and slope shock
    for _ in range(n_months):
        dol_shock = rng.gauss(0.0, 0.025)
        hml_shock = rng.gauss(0.0, 0.018)

        # Monthly return per portfolio k in 0..4
        month_p: list[float] = []
        for k in range(n_portfolios):
            # Monotonic carry yield from -3% to +5% annualized
            carry_yield = (-0.03 + k * 0.02) / 12.0
            # Level factor beta = 1.0; Slope factor beta increases from -0.5 to +0.5
            beta_slope = -0.5 + k * 0.25
            idio = rng.gauss(0.0, 0.006)
            ret = carry_yield + 1.0 * dol_shock + beta_slope * hml_shock + idio
            month_p.append(ret)
        portfolio_returns.append(month_p)

    # Build factors:
    # DOL = mean of all 5 portfolios
    # HML = Portfolio 5 minus Portfolio 1
    dol_factor: list[float] = []
    hml_factor: list[float] = []

    for t in range(n_months):
        row = portfolio_returns[t]
        dol_val = sum(row) / n_portfolios
        hml_val = row[-1] - row[0]
        dol_factor.append(dol_val)
        hml_factor.append(hml_val)

    # Regress each portfolio k on constant, DOL, and HML
    # Design matrix: [1, DOL, HML]
    reg_results: list[dict[str, float]] = []

    # Helper bivariate OLS
    for k in range(n_portfolios):
        y = [portfolio_returns[t][k] for t in range(n_months)]
        x1 = dol_factor
        x2 = hml_factor

        # Means
        my = sum(y) / n_months
        m1 = sum(x1) / n_months
        m2 = sum(x2) / n_months

        # Centered moments
        s11 = sum((x - m1) ** 2 for x in x1)
        s22 = sum((x - m2) ** 2 for x in x2)
        s12 = sum((x1[t] - m1) * (x2[t] - m2) for t in range(n_months))
        sy1 = sum((y[t] - my) * (x1[t] - m1) for t in range(n_months))
        sy2 = sum((y[t] - my) * (x2[t] - m2) for t in range(n_months))

        det = s11 * s22 - s12 * s12
        b1 = (s22 * sy1 - s12 * sy2) / det
        b2 = (s11 * sy2 - s12 * sy1) / det
        alpha = my - b1 * m1 - b2 * m2

        fitted = [alpha + b1 * x1[t] + b2 * x2[t] for t in range(n_months)]
        ss_tot = sum((y[t] - my) ** 2 for t in range(n_months))
        ss_res = sum((y[t] - fitted[t]) ** 2 for t in range(n_months))
        r2 = 1.0 - (ss_res / ss_tot)

        reg_results.append(
            {
                "portfolio": k + 1,
                "ann_mean": round(my * 12.0 * 100, 2),
                "beta_dol": round(b1, 3),
                "beta_hml": round(b2, 3),
                "r_squared": round(r2, 3),
            }
        )

    return {
        "n_months": n_months,
        "ann_mean_dol": round(sum(dol_factor) / n_months * 12.0 * 100, 2),
        "ann_mean_hml": round(sum(hml_factor) / n_months * 12.0 * 100, 2),
        "portfolios": reg_results,
    }


def main() -> None:
    res = simulate_factor_decomposition(n_months=120, seed=42)
    print("=== Lustig-Roussanov-Verdelhan Factor Decomposition ===")
    print(f"Sample: {res['n_months']} months | DOL Mean: {res['ann_mean_dol']}% | HML Mean: {res['ann_mean_hml']}%")
    print("Port | Mean Return | Beta (DOL) | Beta (HML) | R^2")
    print("--------------------------------------------------")
    for p in res["portfolios"]:
        ret_s = f"{p['ann_mean']:>9.2f}%"
        b_dol = f"{p['beta_dol']:>10.3f}"
        b_hml = f"{p['beta_hml']:>10.3f}"
        r2_s = f"{p['r_squared']:>5.3f}"
        print(f"P{p['portfolio']:<4}| {ret_s} | {b_dol} | {b_hml} | {r2_s}")


main()
