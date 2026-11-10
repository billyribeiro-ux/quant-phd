"""Lab F1-L06-1: Portfolio Weighting Schemes & Monthly Rebalancing Mechanics.

Compares value-weighted versus equal-weighted equity portfolios, measuring
weight drift, monthly rebalancing turnover, and bid-ask bounce drag.
"""

from __future__ import annotations

import numpy as np


def simulate_weighting_and_rebalancing(seed: int = 99) -> dict[str, float]:
    """Simulate 12 months of portfolio rebalancing under VW and EW schemes."""
    rng = np.random.default_rng(seed)
    n_stocks = 50
    n_months = 12

    # Initial market capitalizations (highly skewed lognormal)
    init_caps = rng.lognormal(mean=5.0, sigma=1.2, size=n_stocks)
    _vw_init_weights = init_caps / np.sum(init_caps)
    _ew_init_weights = np.full(n_stocks, 1.0 / n_stocks)

    # Monthly stock returns with cross-sectional dispersion and bid-ask bounce
    # Simulate true return + bounce shock: r_{i,t} = mu + shock_t - shock_{t-1}
    bounce_noise = rng.normal(0.0, 0.015, size=(n_months + 1, n_stocks))
    fundamental_returns = rng.normal(0.008, 0.08, size=(n_months, n_stocks))

    cum_ret_vw = 1.0
    cum_ret_ew = 1.0
    turnover_vw_total = 0.0
    turnover_ew_total = 0.0

    current_caps = np.copy(init_caps)

    for t in range(n_months):
        # Observed gross return including microstructure bounce
        r_t = fundamental_returns[t] + (bounce_noise[t + 1] - bounce_noise[t])

        # Value-weighted return for month t (using beginning-of-month caps)
        vw_weights_t = current_caps / np.sum(current_caps)
        vw_port_ret = float(np.sum(vw_weights_t * r_t))
        cum_ret_vw *= 1.0 + vw_port_ret

        # Under buy-and-hold value-weighting, market cap naturally drifts with price:
        current_caps *= 1.0 + r_t
        _vw_end_weights = current_caps / np.sum(current_caps)
        # Turnover in VW is zero if no external rebalancing occurs (only dividends/splits cause turnover)
        turnover_vw_total += 0.0

        # Equal-weighted return for month t
        ew_weights_t = np.full(n_stocks, 1.0 / n_stocks)
        ew_port_ret = float(np.sum(ew_weights_t * r_t))
        cum_ret_ew *= 1.0 + ew_port_ret

        # At month-end, EW weights drift to: w_i * (1 + r_i) / (1 + r_ew)
        ew_end_weights = (ew_weights_t * (1.0 + r_t)) / (1.0 + ew_port_ret)
        # To restore equal weights (1/N), must trade: sum(|w_end - 1/N|) / 2
        monthly_ew_turnover = float(np.sum(np.abs(ew_end_weights - ew_weights_t)) / 2.0)
        turnover_ew_total += monthly_ew_turnover

    annual_turnover_ew_pct = (turnover_ew_total / n_months) * 12.0 * 100.0
    cum_return_vw_pct = (cum_ret_vw - 1.0) * 100.0
    cum_return_ew_pct = (cum_ret_ew - 1.0) * 100.0

    return {
        "n_stocks": n_stocks,
        "n_months": n_months,
        "cum_return_vw_pct": round(cum_return_vw_pct, 2),
        "cum_return_ew_pct": round(cum_return_ew_pct, 2),
        "monthly_turnover_ew_pct": round((turnover_ew_total / n_months) * 100.0, 2),
        "annual_turnover_ew_pct": round(annual_turnover_ew_pct, 1),
    }


def main() -> None:
    print("Lab F1-L06-1 | Portfolio Weighting & Rebalancing Simulator")
    print("----------------------------------------------------------")
    res = simulate_weighting_and_rebalancing(seed=99)
    print(f"Portfolio size:                         {res['n_stocks']} stocks over {res['n_months']} months")
    print(f"Value-Weighted 12-Month Return:         {res['cum_return_vw_pct']:.2f}%")
    print(f"Equal-Weighted 12-Month Return:         {res['cum_return_ew_pct']:.2f}%")
    print(f"Equal-Weighted Monthly Rebalancing Turnover: {res['monthly_turnover_ew_pct']:.2f}% / month")
    print(f"Equal-Weighted Annual Rebalancing Turnover:  {res['annual_turnover_ew_pct']:.1f}% p.a.")


main()
