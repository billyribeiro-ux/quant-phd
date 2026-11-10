"""Lab F4-L03-1: Multi-Metric Factor Crowding Index.

Constructs an empirical factor crowding metric combining pairwise active return
correlation, short interest concentration in the short leg, and valuation spread
distortion, evaluating its ability to forecast factor drawdown risk.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(101)
    n_months = 120  # 10 years of factor monitoring

    # 1. Pairwise Active Correlation across 8 peer quantitative funds
    # In uncrowded regimes: avg pairwise correlation rho ~ 0.25
    # In crowded regimes: rho surges to 0.75 as funds converge on identical signals
    corr_series = np.zeros(n_months)

    # 2. Short Interest Ratio (Days to Cover) in factor short leg
    # Uncrowded: 3.5 days; Crowded: 9.5 days
    short_interest = np.zeros(n_months)

    # 3. Factor Valuation Spread (P/B multiple of longs vs shorts normalized z-score)
    val_spread_z = np.zeros(n_months)

    # Simulate periods with two crowding bubbles (months 40..55 and 90..105)
    crowding_regime = np.zeros(n_months)
    crowding_regime[40:55] = 1.0
    crowding_regime[90:105] = 1.0

    for t in range(n_months):
        if crowding_regime[t] == 1.0:
            corr_series[t] = rng.uniform(0.65, 0.85)
            short_interest[t] = rng.uniform(8.0, 11.5)
            val_spread_z[t] = rng.uniform(1.8, 2.6)
        else:
            corr_series[t] = rng.uniform(0.15, 0.40)
            short_interest[t] = rng.uniform(2.5, 4.8)
            val_spread_z[t] = rng.uniform(-0.8, 0.8)

    # Standardize components into z-scores
    z_corr = (corr_series - np.mean(corr_series)) / np.std(corr_series)
    z_si = (short_interest - np.mean(short_interest)) / np.std(short_interest)
    z_val = (val_spread_z - np.mean(val_spread_z)) / np.std(val_spread_z)

    # Composite Factor Crowding Index (equal-weighted z-score)
    crowding_index = (z_corr + z_si + z_val) / 3.0

    # Simulate forward 3-month factor drawdowns
    # Uncrowded forward drawdown: 2-4%
    # Crowded forward drawdown (unwind risk): 12-25%
    fwd_drawdown = np.zeros(n_months)
    for t in range(n_months):
        if crowding_index[t] > 1.0:
            fwd_drawdown[t] = rng.uniform(0.12, 0.26)
        else:
            fwd_drawdown[t] = rng.uniform(0.01, 0.06)

    # High vs Low Crowding Regime Performance
    high_crowd_mask = crowding_index > 0.80
    low_crowd_mask = crowding_index <= 0.80

    avg_dd_high = float(np.mean(fwd_drawdown[high_crowd_mask]))
    avg_dd_low = float(np.mean(fwd_drawdown[low_crowd_mask]))
    corr_crowd_dd = float(np.corrcoef(crowding_index, fwd_drawdown)[0, 1])

    print("=== FACTOR CROWDING INDEX AND UNWIND RISK ===")
    print(f"Low Crowding Months:  N={np.sum(low_crowd_mask)}, Avg Fwd 3M Drawdown={avg_dd_low:.2%}")
    print(f"High Crowding Months: N={np.sum(high_crowd_mask)}, Avg Fwd 3M Drawdown={avg_dd_high:.2%}")
    print(f"Crowding vs Future Drawdown Correlation: {corr_crowd_dd:.3f}")
    print(f"Peak Crowding Index Score: {np.max(crowding_index):.2f} (Month {np.argmax(crowding_index)})")


main()
