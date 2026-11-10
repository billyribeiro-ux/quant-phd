"""Lab X2-L02-1: Carry Crash Risk & Asymmetric Liquidity Spiral Simulator.

Simulates endogenous margin constraints, forced unwinding, and negative skewness
in currency carry trades (Brunnermeier, Nagel & Pedersen 2008).
"""

from __future__ import annotations

import math
import random


def simulate_liquidity_spiral(
    n_days: int = 500,
    seed: int = 101,
) -> dict[str, float]:
    """Simulate carry trade returns under margin constraints and feedback unwinding.

    Args:
        n_days: Number of simulated trading days.
        seed: Random seed.

    Returns:
        Summary metrics including mean return, volatility, skewness, and kurtosis.
    """
    rng = random.Random(seed)

    daily_carry_yield = 0.0003  # approx 7.5% annualized interest rate spread
    capital = 1.0  # trader net worth
    max_leverage = 5.0
    position = capital * max_leverage  # target size
    market_depth = 40.0  # liquidity parameter

    returns: list[float] = []
    vol = 0.005

    for _ in range(n_days):
        # Stochastic volatility clustering
        vol = max(0.003, min(0.025, 0.94 * vol + 0.06 * 0.005 + rng.gauss(0.0, 0.001)))
        fund_shock = rng.gauss(0.0, vol)
        gross_ret = daily_carry_yield + fund_shock

        # Mark-to-market capital update
        capital_change = position * gross_ret
        capital = max(0.05, capital + capital_change)

        # Margin constraint: max_position = capital * max_leverage
        max_pos = capital * max_leverage
        unwind_flow = 0.0

        if position > max_pos:
            # Margin call: forced deleveraging
            unwind_flow = position - max_pos
            position = max_pos
        else:
            # Re-leveraging towards target
            position = min(max_pos, position + 0.1 * (max_pos - position))

        # Price impact from fire sales
        price_impact = -unwind_flow / market_depth
        net_ret = gross_ret + price_impact
        returns.append(net_ret)

    # Calculate sample moments
    n = len(returns)
    mean_ret = sum(returns) / n
    var_ret = sum((r - mean_ret) ** 2 for r in returns) / (n - 1)
    std_ret = math.sqrt(var_ret)

    # Sample skewness (gamma_3) and kurtosis (gamma_4)
    m3 = sum((r - mean_ret) ** 3 for r in returns) / n
    m4 = sum((r - mean_ret) ** 4 for r in returns) / n
    skewness = m3 / (std_ret**3)
    kurtosis = m4 / (std_ret**4)

    return {
        "n_days": float(n_days),
        "mean_daily_ret": round(mean_ret, 5),
        "ann_vol": round(std_ret * math.sqrt(252), 4),
        "skewness": round(skewness, 4),
        "kurtosis": round(kurtosis, 4),
    }


def main() -> None:
    res = simulate_liquidity_spiral(n_days=500, seed=101)
    print("=== Carry Crash Risk & Liquidity Spiral Simulation ===")
    print(f"Sample length: {int(res['n_days'])} days")
    print(f"Daily mean return: {res['mean_daily_ret'] * 100:.3f}%")
    print(f"Annualized volatility: {res['ann_vol'] * 100:.2f}%")
    print(f"Sample skewness (gamma_3): {res['skewness']:.3f}")
    print(f"Sample kurtosis (gamma_4): {res['kurtosis']:.3f}")


main()
