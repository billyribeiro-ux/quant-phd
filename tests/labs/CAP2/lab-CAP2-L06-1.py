"""Lab CAP2-L06-1: Empirical tests for the Fiscal Theory of the Price Level and HFT market quality.

Implements Cochrane (2023) fiscal surplus valuation equation inflation accounting,
and Hasbrouck (1991) / Brogaard et al. (2014) high-frequency quote-to-trade and
effective spread decomposition.
"""

from __future__ import annotations

import numpy as np


def ftpl_inflation_accounting(
    debt_gdp_ratio: float,
    fiscal_shock_pct_gdp: float,
    expected_surplus_response: float,
    real_rate: float = 0.015,
) -> tuple[float, float, float]:
    """Decompose inflation shock under Fiscal Theory of the Price Level (Cochrane 2023).

    B_{t-1}/P_t = E_t sum beta^j s_{t+j}.
    Unbacked fiscal expansion Delta s_unbacked = Delta d - Delta E[sum s].
    Price level impulse: Delta P / P = Delta s_unbacked / (B/P).
    """
    unbacked_expansion = fiscal_shock_pct_gdp - expected_surplus_response
    implied_inflation = unbacked_expansion / debt_gdp_ratio
    return unbacked_expansion, implied_inflation, debt_gdp_ratio


def evaluate_hft_market_quality(
    quote_updates: np.ndarray,
    trade_counts: np.ndarray,
    effective_spreads_bps: np.ndarray,
    realized_spreads_bps: np.ndarray,
) -> tuple[float, float, float, float]:
    """Compute quote-to-trade ratio, effective spread, and adverse selection cost."""
    # Quote-to-trade ratio
    q_to_t = float(np.sum(quote_updates) / np.sum(trade_counts))

    mean_eff = float(np.mean(effective_spreads_bps))
    mean_real = float(np.mean(realized_spreads_bps))
    # Price impact / adverse selection: Effective spread - Realized spread
    adverse_selection = mean_eff - mean_real

    return q_to_t, mean_eff, mean_real, adverse_selection


def main() -> None:
    # 1. Resolution 11: FTPL and 2021-2023 Inflation
    # US Debt/GDP ~ 100% (1.0). Total pandemic fiscal transfers ~ $5T (20% of GDP).
    # If primary surpluses are expected to cover 40% of the stimulus, unbacked is 12% of GDP.
    debt_gdp = 1.00
    fiscal_shock = 0.20  # 20% of GDP
    surplus_backed = 0.08  # 8% of GDP backed by future surpluses

    unbacked, cum_inflation, _ = ftpl_inflation_accounting(debt_gdp, fiscal_shock, surplus_backed)

    print("--- Resolution 11: FTPL Explains 2021-2023 Inflation ---")
    print(f"Initial Debt-to-GDP Ratio:        {debt_gdp * 100.0:.1f}%")
    print(f"Total Fiscal Expansion:           {fiscal_shock * 100.0:.1f}% of GDP")
    print(f"Future Backed Primary Surpluses:  {surplus_backed * 100.0:.1f}% of GDP")
    print(f"Unbacked Fiscal Expansion:        {unbacked * 100.0:.1f}% of GDP")
    print(f"FTPL Predicted Cumulative Inflation: {cum_inflation * 100.0:.2f}%")

    # 2. Resolution 12: HFT and Market Quality
    # 100 trading sessions across modern electronic limit order books
    rng = np.random.default_rng(2014)
    trades = rng.integers(5000, 20000, size=100)
    # HFT quote-to-trade ratio typically 20:1 to 60:1
    quote_mult = rng.uniform(25.0, 50.0, size=100)
    quotes = (trades * quote_mult).astype(np.int64)

    eff_spreads = rng.normal(3.2, 0.4, size=100)  # bps
    real_spreads = rng.normal(1.1, 0.3, size=100)  # bps

    q_ratio, eff_s, real_s, adv_sel = evaluate_hft_market_quality(quotes, trades, eff_spreads, real_spreads)

    print("\n--- Resolution 12: Does HFT Improve Market Quality? ---")
    print(f"Aggregate Quote-to-Trade Ratio: {q_ratio:.1f} : 1")
    print(f"Average Effective Spread:      {eff_s:.2f} bps")
    print(f"Average Realized Spread:       {real_s:.2f} bps")
    print(f"Informed Adverse Selection:    {adv_sel:.2f} bps")
    print(f"Net Liquidity Assessment:      {'LIQUIDITY ENHANCING' if eff_s < 5.0 else 'TOXIC'}")


main()
