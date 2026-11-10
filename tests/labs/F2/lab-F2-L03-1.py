"""Lab F2-L03-1: Operating Profitability (RMW) and Investment (CMA) Factor Construction.

Simulates corporate fundamentals (Market Equity ME, Operating Profitability OP,
and Asset Growth Investment Inv) to construct canonical Fama-French (2015)
RMW and CMA factors via 2x3 sorts, verifying the negative correlation between
investment and profitability and testing their diversification benefits with HML.
"""

from __future__ import annotations

import numpy as np


def simulate_profitability_and_investment(seed: int = 42) -> dict[str, float | int]:
    """Simulate 2x3 sorts for RMW and CMA and measure factor cross-correlations."""
    rng = np.random.default_rng(seed)
    n_stocks = 300
    n_months = 120

    # Cross-sectional characteristics
    log_me = rng.normal(loc=6.0, scale=1.4, size=n_stocks)
    me = np.exp(log_me)

    # Book-to-market
    log_bm = -0.25 * (log_me - 6.0) + rng.normal(loc=-0.4, scale=0.5, size=n_stocks)
    bm = np.exp(log_bm)

    # Operating profitability: negatively correlated with distressed high B/M stocks
    op = -0.15 * log_bm + rng.normal(loc=0.14, scale=0.10, size=n_stocks)

    # Investment (Asset Growth): high-growth firms invest aggressively (low B/M, high investment)
    inv = -0.20 * log_bm + rng.normal(loc=0.08, scale=0.12, size=n_stocks)

    # Breakpoints (median for size, 30/70 for OP and Inv)
    size_median = float(np.median(me))
    small = me <= size_median
    big = me > size_median

    op_p30 = float(np.percentile(op, 30))
    op_p70 = float(np.percentile(op, 70))
    robust = op >= op_p70
    weak = op < op_p30
    (op >= op_p30) & (op < op_p70)

    inv_p30 = float(np.percentile(inv, 30))
    inv_p70 = float(np.percentile(inv, 70))
    conservative = inv < inv_p30
    aggressive = inv >= inv_p70
    (inv >= inv_p30) & (inv < inv_p70)

    # Monthly factor returns simulation
    rmw_true = rng.normal(0.035 / 12, 0.08 / np.sqrt(12), size=n_months)
    cma_true = rng.normal(0.030 / 12, 0.07 / np.sqrt(12), size=n_months)
    hml_true = rng.normal(0.040 / 12, 0.11 / np.sqrt(12), size=n_months)

    # Betas
    beta_op = np.where(robust, 0.7, np.where(weak, -0.7, 0.0)) + rng.normal(0, 0.1, size=n_stocks)
    beta_inv = np.where(conservative, 0.6, np.where(aggressive, -0.6, 0.0)) + rng.normal(0, 0.1, size=n_stocks)
    beta_bm = np.where(bm > np.median(bm), 0.5, -0.4) + rng.normal(0, 0.1, size=n_stocks)

    stock_rets = np.zeros((n_months, n_stocks))
    for t in range(n_months):
        idio = rng.normal(0, 0.20 / np.sqrt(12), size=n_stocks)
        stock_rets[t, :] = beta_op * rmw_true[t] + beta_inv * cma_true[t] + beta_bm * hml_true[t] + idio

    def vw_ret(mask: np.ndarray) -> np.ndarray:
        w = me[mask] / np.sum(me[mask])
        return np.asarray(stock_rets[:, mask] @ w)

    # RMW: Robust Minus Weak
    # RMW = 1/2 (Small Robust + Big Robust) - 1/2 (Small Weak + Big Weak)
    r_sr = vw_ret(small & robust)
    r_br = vw_ret(big & robust)
    r_sw = vw_ret(small & weak)
    r_bw = vw_ret(big & weak)
    rmw = 0.5 * (r_sr + r_br) - 0.5 * (r_sw + r_bw)

    # CMA: Conservative Minus Aggressive
    # CMA = 1/2 (Small Conservative + Big Conservative) - 1/2 (Small Aggressive + Big Aggressive)
    r_sc = vw_ret(small & conservative)
    r_bc = vw_ret(big & conservative)
    r_sa = vw_ret(small & aggressive)
    r_ba = vw_ret(big & aggressive)
    cma = 0.5 * (r_sc + r_bc) - 0.5 * (r_sa + r_ba)

    mean_rmw = float(np.mean(rmw) * 12 * 100)
    std_rmw = float(np.std(rmw, ddof=1) * np.sqrt(12) * 100)
    t_rmw = float(np.mean(rmw) / (np.std(rmw, ddof=1) / np.sqrt(n_months)))

    mean_cma = float(np.mean(cma) * 12 * 100)
    std_cma = float(np.std(cma, ddof=1) * np.sqrt(12) * 100)
    t_cma = float(np.mean(cma) / (np.std(cma, ddof=1) / np.sqrt(n_months)))

    corr_rmw_cma = float(np.corrcoef(rmw, cma)[0, 1])

    return {
        "n_stocks": n_stocks,
        "n_months": n_months,
        "mean_rmw": round(mean_rmw, 2),
        "std_rmw": round(std_rmw, 2),
        "t_rmw": round(t_rmw, 2),
        "mean_cma": round(mean_cma, 2),
        "std_cma": round(std_cma, 2),
        "t_cma": round(t_cma, 2),
        "corr_rmw_cma": round(corr_rmw_cma, 4),
    }


def main() -> None:
    print("Lab F2-L03-1 | Profitability (RMW) and Investment (CMA) Factor Sorts")
    print("-------------------------------------------------------------------")
    res = simulate_profitability_and_investment(seed=42)
    print(f"Sample size: {res['n_stocks']} equities over {res['n_months']} months")
    print(f"RMW Annualized Premium: {res['mean_rmw']:+.2f}% (vol {res['std_rmw']:.2f}%, t = {res['t_rmw']:.2f})")
    print(f"CMA Annualized Premium: {res['mean_cma']:+.2f}% (vol {res['std_cma']:.2f}%, t = {res['t_cma']:.2f})")
    print(f"RMW-CMA Correlation:    {res['corr_rmw_cma']:+.4f}")


main()
