"""Lab F4-L02-1: The August 2007 Quant Quake and Fire-Sale Contagion.

Simulates the multi-strategy fire-sale cascade modeled by Khandani & Lo (2011):
a primary fund unwinds long-short equity factor portfolios to meet external margin calls,
generating temporary price impact that triggers margin breaches and forced deleveraging
at unexposed peer funds, followed by liquidity recovery.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # 5 Quantitative Equity Market-Neutral (QMN) funds trading N=100 common factor stocks
    n_stocks = 100
    n_funds = 5
    initial_equity = 100.0  # $100M each
    leverage = 4.0  # 4x gross leverage -> $400M long, $400M short

    # Kyle's lambda price impact: price move per $1M liquidated
    # Linear price impact: Delta P / P = - lambda * Q_sell
    lambda_impact = 0.00015  # 1.5 bps per $1M order

    # Common factor portfolio: stocks 0..49 are Longs, 50..99 are Shorts
    long_stocks = slice(0, 50)
    short_stocks = slice(50, 100)

    # Days: Day 0 (pre-crisis), Day 1 (Fund 1 subprime liquidation),
    # Day 2 (contagion liquidation), Day 3 (overshoot), Day 4 (rebound)
    n_days = 5
    prices = np.ones((n_days, n_stocks))
    fund_equities = np.zeros((n_days, n_funds))
    fund_equities[0] = initial_equity

    # Daily liquidation volume:
    # Day 1: Fund 1 faces outside mortgage margin call and liquidates 50% of its equity book
    # Day 2: Margin breach triggers liquidation from Fund 2 and Fund 3
    # Day 3: Exhaustion of selling pressure
    # Day 4: Value buyers enter; prices mean-revert 85% of distortion
    liquidations_long = np.zeros((n_days, n_stocks))
    liquidations_short = np.zeros((n_days, n_stocks))

    # Day 1: Fund 1 liquidates $200M longs and buys back $200M shorts ($4M per stock)
    liquidations_long[1, long_stocks] = 4.0
    liquidations_short[1, short_stocks] = 4.0

    # Day 2: Secondary margin liquidations from Fund 2 and 3 ($6M per stock)
    liquidations_long[2, long_stocks] = 6.0
    liquidations_short[2, short_stocks] = 6.0

    # Day 4: Rebound buying (shorts sold, longs bought)
    rebound_fraction = 0.80

    cum_long_impact = 0.0
    cum_short_impact = 0.0

    for d in range(1, n_days):
        if d < 4:
            # Impact on longs: selling depresses price
            # Impact on shorts: buying back raises price
            q_long = np.mean(liquidations_long[d, long_stocks])
            q_short = np.mean(liquidations_short[d, short_stocks])
            cum_long_impact -= float(lambda_impact * q_long * 50.0)  # aggregate basket impact
            cum_short_impact += float(lambda_impact * q_short * 50.0)
        else:
            # Day 4: Mean reversion / liquidity return
            cum_long_impact *= 1.0 - rebound_fraction
            cum_short_impact *= 1.0 - rebound_fraction

        prices[d, long_stocks] = 1.0 + cum_long_impact
        prices[d, short_stocks] = 1.0 + cum_short_impact

        # Calculate fund equity for an unleveraged bystander vs a 4x levered fund
        # Return on factor book = r_long - r_short
        r_long = prices[d, 0] / prices[d - 1, 0] - 1.0
        r_short = prices[d, 50] / prices[d - 1, 50] - 1.0
        daily_factor_ret = r_long - r_short

        for f in range(n_funds):
            # Fund equity evolves with levered factor return
            fund_equities[d, f] = fund_equities[d - 1, f] * (1.0 + leverage * daily_factor_ret)

    print("=== AUGUST 2007 QUANT QUAKE LIQUIDATION SIMULATION ===")
    print(f"Day 0 (Baseline):  Factor Spread = 0.00%, Fund Equity = ${fund_equities[0, 0]:.1f}M")
    print(
        f"Day 1 (Fund 1 Unwind): Longs={prices[1, 0] - 1:+.2%}, Shorts={prices[1, 50] - 1:+.2%}, "
        f"Fund Equity = ${fund_equities[1, 1]:.1f}M (-{(1 - fund_equities[1, 1] / initial_equity):.1%})"
    )
    print(
        f"Day 2 (Fire Sale Spiral): Longs={prices[2, 0] - 1:+.2%}, Shorts={prices[2, 50] - 1:+.2%}, "
        f"Fund Equity = ${fund_equities[2, 1]:.1f}M (-{(1 - fund_equities[2, 1] / initial_equity):.1%})"
    )
    print(
        f"Day 4 (August 10 Rebound): Longs={prices[4, 0] - 1:+.2%}, Shorts={prices[4, 50] - 1:+.2%}, "
        f"Fund Equity = ${fund_equities[4, 1]:.1f}M"
    )


main()
