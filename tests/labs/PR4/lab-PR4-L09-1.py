"""Lab 9: FRTB Liquidity Horizons and Basel P&L Attribution Testing (PLAT).

Demonstrates the BCBS Fundamental Review of the Trading Book (FRTB) standards:
scaled liquidity horizons and the dual PLAT test (Spearman rank correlation and variance ratio).
"""

from __future__ import annotations

import math

import numpy as np
import scipy.stats


def main() -> None:
    rng = np.random.default_rng(42)

    # 1. FRTB Liquidity Horizon Scaled Expected Shortfall Calculation
    # Liquidity horizons: LH1 = 10, LH2 = 20, LH3 = 40, LH4 = 60, LH5 = 120 days
    # Sub-portfolio ES estimates at base 10-day level for progressive factor subsets:
    es_subsets = [150_000.0, 190_000.0, 240_000.0, 280_000.0, 310_000.0]
    horizons = [10, 20, 40, 60, 120]

    # FRTB Aggregation Formula:
    # ES = sqrt( sum_{j=1}^5 (ES_j)^2 * (LH_j - LH_{j-1}) / 10 ) where LH_0 = 0
    es_sq_sum = 0.0
    lh_prev = 0
    for es_j, lh_j in zip(es_subsets, horizons, strict=True):
        weight = (lh_j - lh_prev) / 10.0
        es_sq_sum += (es_j**2) * weight
        lh_prev = lh_j

    es_frtb_total = math.sqrt(es_sq_sum)

    print("FRTB Liquidity Horizon Expected Shortfall Aggregation:")
    for j, (lh, es_val) in enumerate(zip(horizons, es_subsets, strict=True), start=1):
        print(f"  Level {j} (LH = {lh:3d} days): ES(T_{j}) = ${es_val:,.2f}")
    print(f"FRTB Total Scaled Market Risk Capital ES: ${es_frtb_total:,.2f}")
    print("=" * 70)

    # 2. Basel P&L Attribution Test (PLAT)
    # Compare 250 daily observations of Hypothetical P&L (HPL) vs Risk-Theoretical P&L (RTPL)
    t_days = 250
    hpl = rng.normal(loc=15_000.0, scale=120_000.0, size=t_days)
    # Model tracking noise (representing un-modellable basis risks and simplifications)
    tracking_noise = rng.normal(loc=0.0, scale=18_000.0, size=t_days)
    rtpl = hpl + tracking_noise

    # Metric 1: Spearman rank correlation (Green zone: >= 0.80)
    spearman_corr, _ = scipy.stats.spearmanr(hpl, rtpl)
    # Metric 2: Variance ratio Var(RTPL - HPL) / Var(HPL) (Green zone: <= 0.20)
    diff_var = float(np.var(rtpl - hpl, ddof=1))
    hpl_var = float(np.var(hpl, ddof=1))
    var_ratio = diff_var / hpl_var

    is_green = bool(spearman_corr >= 0.80 and var_ratio <= 0.20)

    print("Basel III P&L Attribution Test (PLAT) Results (T = 250 trading days):")
    print(f"  Spearman Rank Correlation r_S: {float(spearman_corr):.4f} (Threshold >= 0.80)")
    print(f"  Unexplained Variance Ratio VR:  {var_ratio:.4f} (Threshold <= 0.20)")
    print(f"  Trading Desk Assessment:        {'GREEN ZONE (IMA Approved)' if is_green else 'AMBER/RED ZONE'}")


main()
