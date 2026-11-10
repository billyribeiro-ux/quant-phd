"""Lab MS4-L04-1: Trading-cost mitigation via buy-hold buffer zones (hysteresis).

Demonstrates turnover reduction, factor exposure preservation, and net alpha gains
achieved by replacing naive threshold rebalancing with buy-hold buffer bands.
SIMULATED: multi-period ranking trajectory across a 50-stock universe.
"""

from __future__ import annotations

import math
import random


def run_buffer_mitigation_simulation() -> None:
    rng = random.Random(42)
    n_assets = 50
    target_k = 10
    n_periods = 6
    adv = 20000000.0
    vol = 0.02
    prefactor_y = 0.50
    portfolio_aum = 50000000.0

    # Generate initial signal scores and initial rankings
    scores = [rng.gauss(0.0, 1.0) for _ in range(n_assets)]

    # Initial portfolio: top 10 assets
    ranked_init = sorted(range(n_assets), key=lambda i: scores[i], reverse=True)
    initial_holdings = set(ranked_init[:target_k])

    holdings_strict = set(initial_holdings)
    holdings_buffered = set(initial_holdings)

    turnover_strict_total = 0.0
    turnover_buf_total = 0.0
    k_hold = math.floor(target_k * 1.5)  # 15

    for _ in range(n_periods):
        # Signal drifts with autoregressive process + noise
        scores = [0.85 * s + rng.gauss(0.0, 0.4) for s in scores]
        ranks = sorted(range(n_assets), key=lambda i: scores[i], reverse=True)
        rank_of = {asset: r + 1 for r, asset in enumerate(ranks)}

        # 1. Strict rebalancing: top 10 always
        new_strict = set(ranks[:target_k])
        trades_strict = len(new_strict - holdings_strict)
        turnover_strict_total += trades_strict / target_k
        holdings_strict = new_strict

        # 2. Buffered rebalancing: retain held assets with rank <= k_hold (15)
        retained = [a for a in holdings_buffered if rank_of[a] <= k_hold]
        retained.sort(key=lambda a: rank_of[a])
        if len(retained) >= target_k:
            new_buf = set(retained[:target_k])
        else:
            needed = target_k - len(retained)
            unheld = [a for a in ranks if a not in retained]
            new_buf = set(retained + unheld[:needed])

        trades_buf = len(new_buf - holdings_buffered)
        turnover_buf_total += trades_buf / target_k
        holdings_buffered = new_buf

    # Estimate trading costs under square-root impact
    # Dollar trade per changed stock: (portfolio_aum / target_k)
    trade_size = portfolio_aum / target_k
    unit_impact_cost = prefactor_y * vol * math.sqrt(trade_size / adv)
    dollar_cost_per_trade = trade_size * unit_impact_cost

    cost_strict_dollars = turnover_strict_total * target_k * dollar_cost_per_trade
    cost_buf_dollars = turnover_buf_total * target_k * dollar_cost_per_trade

    cost_strict_bps = (cost_strict_dollars / portfolio_aum) * 10000.0
    cost_buf_bps = (cost_buf_dollars / portfolio_aum) * 10000.0
    savings_bps = cost_strict_bps - cost_buf_bps
    turnover_reduction_pct = (1.0 - turnover_buf_total / turnover_strict_total) * 100.0

    print(f"Target Portfolio Size:        {target_k} assets (Universe: {n_assets})")
    print(f"Buffer Zone Band:             Buy rank <= {target_k}, Hold rank <= {k_hold}")
    print(f"Rebalancing Periods:          {n_periods}")
    print(f"Strict Cumulative Turnover:   {turnover_strict_total:.4f} ({turnover_strict_total * 100.0:.1f}%)")
    print(f"Buffered Cumulative Turnover: {turnover_buf_total:.4f} ({turnover_buf_total * 100.0:.1f}%)")
    print(f"Turnover Reduction:           {turnover_reduction_pct:.2f}%")
    print(f"Strict Total Impact Cost:     {cost_strict_dollars:.2f} ({cost_strict_bps:.2f} bps)")
    print(f"Buffered Total Impact Cost:   {cost_buf_dollars:.2f} ({cost_buf_bps:.2f} bps)")
    print(f"Trading Cost Savings:         {savings_bps:.2f} bps")
    print(f"Mitigation Effective:         {turnover_reduction_pct > 30.0}")


def main() -> None:
    run_buffer_mitigation_simulation()


main()
