"""Lab F1-L04-1: Portfolio Sorting Methodology & Univariate/Bivariate Sorts.

Simulates univariate quintile sorts and bivariate 2x3 independent and
conditional portfolio sorts, computing spread returns and cell occupancy.
"""

from __future__ import annotations

import numpy as np


def simulate_portfolio_sorts(seed: int = 55) -> dict[str, float | int]:
    """Execute univariate quintiles and bivariate 2x3 sorts on a cross-section."""
    rng = np.random.default_rng(seed)
    n_stocks = 250

    # Simulate firm size (market equity) and book-to-market signal
    size = rng.lognormal(mean=6.0, sigma=1.5, size=n_stocks)
    bm = rng.lognormal(mean=-0.2, sigma=0.7, size=n_stocks)

    # Correlated returns: positive value premium and size premium
    base_ret = rng.normal(0.01, 0.05, size=n_stocks)
    value_tilt = 0.025 * (np.log(bm) - np.mean(np.log(bm)))
    size_tilt = -0.015 * (np.log(size) - np.mean(np.log(size)))
    returns = base_ret + value_tilt + size_tilt

    # 1. Univariate sort on Book-to-Market into quintiles
    bm_cuts = np.percentile(bm, [20.0, 40.0, 60.0, 80.0])
    q_assign = np.digitize(bm, bm_cuts)

    q_returns = [float(np.mean(returns[q_assign == q])) for q in range(5)]
    univariate_spread = q_returns[4] - q_returns[0]

    # 2. Bivariate 2x3 Sort: Size (Small/Big) x BM (Low/Neutral/High)
    size_median = float(np.median(size))
    bm_p30, bm_p70 = float(np.percentile(bm, 30.0)), float(np.percentile(bm, 70.0))

    # Independent 2x3 grid
    grid_indep = np.zeros((2, 3), dtype=np.float64)
    counts_indep = np.zeros((2, 3), dtype=np.int32)
    for s_idx in range(2):
        s_mask = size <= size_median if s_idx == 0 else size > size_median
        for b_idx in range(3):
            if b_idx == 0:
                b_mask = bm <= bm_p30
            elif b_idx == 1:
                b_mask = (bm > bm_p30) & (bm <= bm_p70)
            else:
                b_mask = bm > bm_p70

            cell_mask = s_mask & b_mask
            counts_indep[s_idx, b_idx] = int(np.sum(cell_mask))
            if np.sum(cell_mask) > 0:
                grid_indep[s_idx, b_idx] = float(np.mean(returns[cell_mask]))

    # Factor spreads from 2x3:
    # HML = 0.5 * (Small_High + Big_High) - 0.5 * (Small_Low + Big_Low)
    hml_factor = 0.5 * (grid_indep[0, 2] + grid_indep[1, 2]) - 0.5 * (grid_indep[0, 0] + grid_indep[1, 0])
    # SMB = (1/3)*(Small_Low + Small_Neutral + Small_High) - (1/3)*(Big_Low + Big_Neutral + Big_High)
    smb_factor = float(np.mean(grid_indep[0, :])) - float(np.mean(grid_indep[1, :]))

    return {
        "n_stocks": n_stocks,
        "q1_bm_return_pct": round(q_returns[0] * 100.0, 2),
        "q5_bm_return_pct": round(q_returns[4] * 100.0, 2),
        "univariate_spread_pct": round(univariate_spread * 100.0, 2),
        "hml_factor_pct": round(hml_factor * 100.0, 2),
        "smb_factor_pct": round(smb_factor * 100.0, 2),
        "min_cell_count": int(np.min(counts_indep)),
        "max_cell_count": int(np.max(counts_indep)),
    }


def main() -> None:
    print("Lab F1-L04-1 | Portfolio Sorting Methodology Simulator")
    print("-------------------------------------------------------")
    res = simulate_portfolio_sorts(seed=55)
    print(f"Total cross-section size:               {res['n_stocks']} stocks")
    print(f"Univariate Q1 (Low BM / Growth) Return: {res['q1_bm_return_pct']:.2f}% / month")
    print(f"Univariate Q5 (High BM / Value) Return: {res['q5_bm_return_pct']:.2f}% / month")
    print(f"Univariate Q5 - Q1 Value Spread:        +{res['univariate_spread_pct']:.2f}% / month")
    print(f"2x3 Fama-French HML Factor Spread:      +{res['hml_factor_pct']:.2f}% / month")
    print(f"2x3 Fama-French SMB Factor Spread:      +{res['smb_factor_pct']:.2f}% / month")
    print(f"2x3 Grid Cell Occupancy Range:          {res['min_cell_count']} to {res['max_cell_count']} stocks")


main()
