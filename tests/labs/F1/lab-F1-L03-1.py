"""Lab F1-L03-1: Delisting Returns & Delisting Bias Correction (Shumway 1997).

Simulates terminal delisting events and evaluates the return distortion
when missing performance delisting returns are omitted versus corrected.
"""

from __future__ import annotations

import numpy as np


def simulate_delisting_bias(seed: int = 77) -> dict[str, float]:
    """Demonstrate the impact of missing delisting returns and Shumway correction."""
    rng = np.random.default_rng(seed)
    n_stocks = 300

    # 1. Base monthly returns before delisting
    raw_returns = rng.normal(loc=0.008, scale=0.06, size=n_stocks)

    # 2. Assign exchanges: 40% NYSE (1), 10% AMEX (2), 50% NASDAQ (3)
    exchange_codes = rng.choice([1, 2, 3], size=n_stocks, p=[0.40, 0.10, 0.50])

    # 3. Delisting events: ~10% of stocks delist this month
    # 70% of delistings are performance-related (codes 500, 520, 560, 584)
    # 30% are mergers (code 200)
    delist_codes = np.full(n_stocks, 100, dtype=np.int32)
    delist_returns = np.full(n_stocks, np.nan, dtype=np.float64)

    delist_idx = rng.choice(n_stocks, size=30, replace=False)
    for idx in delist_idx:
        is_perf = rng.uniform() < 0.70
        if is_perf:
            delist_codes[idx] = int(rng.choice([500, 520, 560, 584]))
            # In CRSP, roughly half of performance delistings historically had missing DLRET
            has_crsp_dlret = rng.uniform() < 0.40
            if has_crsp_dlret:
                # Realized delisting loss
                delist_returns[idx] = rng.uniform(-0.60, -0.20)
            else:
                delist_returns[idx] = np.nan  # MISSING in database!
        else:
            delist_codes[idx] = 200  # merger
            delist_returns[idx] = rng.uniform(0.05, 0.25)  # takeover premium

    # Case A: Naive approach (missing delisting returns treated as 0.0)
    ret_naive = np.copy(raw_returns)
    for i in range(n_stocks):
        if np.isfinite(delist_returns[i]):
            ret_naive[i] = (1.0 + raw_returns[i]) * (1.0 + delist_returns[i]) - 1.0
        # If delist_returns[i] is NaN, naive leaves raw_returns[i] unchanged (implicit 0% delisting return)

    # Case B: Shumway (1997) / Shumway & Sloan (1999) correction
    ret_shumway = np.copy(raw_returns)
    for i in range(n_stocks):
        if np.isfinite(delist_returns[i]):
            ret_shumway[i] = (1.0 + raw_returns[i]) * (1.0 + delist_returns[i]) - 1.0
        elif delist_codes[i] >= 200:
            is_perf = delist_codes[i] == 500 or (520 <= delist_codes[i] <= 584)
            penalty = (-0.55 if exchange_codes[i] == 3 else -0.30) if is_perf else 0.0
            ret_shumway[i] = (1.0 + raw_returns[i]) * (1.0 + penalty) - 1.0

    mean_naive = float(np.mean(ret_naive))
    mean_shumway = float(np.mean(ret_shumway))
    upward_bias_annual = float((mean_naive - mean_shumway) * 12.0 * 100.0)

    # Distress portfolio bias: only stocks that delisted
    delist_naive = float(np.mean(ret_naive[delist_idx]))
    delist_shumway = float(np.mean(ret_shumway[delist_idx]))
    distress_bias_monthly = float((delist_naive - delist_shumway) * 100.0)

    return {
        "n_stocks": n_stocks,
        "n_delistings": len(delist_idx),
        "mean_naive_pct": round(mean_naive * 100.0, 3),
        "mean_shumway_pct": round(mean_shumway * 100.0, 3),
        "annual_bias_pct": round(upward_bias_annual, 3),
        "distress_naive_pct": round(delist_naive * 100.0, 2),
        "distress_shumway_pct": round(delist_shumway * 100.0, 2),
        "distress_bias_pct": round(distress_bias_monthly, 2),
    }


def main() -> None:
    print("Lab F1-L03-1 | Shumway (1997) Delisting Bias Simulator")
    print("------------------------------------------------------")
    res = simulate_delisting_bias(seed=77)
    print(f"Total cross-section size:               {res['n_stocks']} stocks")
    print(f"Delisting events in month:              {res['n_delistings']} events")
    print(f"Naive cross-sectional mean return:      {res['mean_naive_pct']:.3f}% / month")
    print(f"Shumway-corrected mean return:          {res['mean_shumway_pct']:.3f}% / month")
    print(f"Annualized upward bias from omission:   +{res['annual_bias_pct']:.3f}% p.a.")
    print(f"Delisted group return (naive):          {res['distress_naive_pct']:.2f}%")
    print(f"Delisted group return (corrected):      {res['distress_shumway_pct']:.2f}%")
    print(f"Delisting return understatement:        +{res['distress_bias_pct']:.2f}%")


main()
