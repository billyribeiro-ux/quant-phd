"""Instance generator for MS3 project: Atlas A10 execution and cost models.

Deterministic problem instances across seeds 0-49.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic problem instance for MS3 autograder."""
    rng = random.Random(seed)

    total_shares = float(100_000 + ((seed * 17) % 40) * 5_000)
    horizon = float(1.0 + (seed % 5) * 0.25)
    n_steps = 10 + (seed % 11)  # 10 to 20 intervals
    daily_volume = float(2_000_000 + ((seed * 23) % 50) * 100_000)
    daily_volatility = round(0.015 + ((seed * 7) % 25) * 0.001, 5)
    gamma = round(1e-7 + ((seed * 13) % 20) * 1e-8, 10)
    eta = round(5e-7 + ((seed * 19) % 30) * 2e-8, 10)
    risk_aversion = round(1e-6 * (1.0 + (seed % 15) * 0.5), 9)
    resilience = round(1.5 + (seed % 9) * 0.5, 2)

    decision_price = round(100.0 + (seed % 50) * 0.5, 2)
    arrival_drift = round(((seed * 3) % 9 - 4) * 0.05, 3)
    arrival_price = round(decision_price + arrival_drift, 3)

    # Generate multi-slice trades totaling executed_shares <= total_shares
    exec_ratio = 0.85 + (seed % 15) * 0.01  # 85% to 99% fill
    exec_target = total_shares * exec_ratio
    n_trades = 5 + (seed % 6)

    shares_per_trade = exec_target / n_trades
    trades: list[tuple[float, float]] = []
    curr_price = arrival_price
    for _ in range(n_trades):
        # Slices experience temporary and permanent impact drift
        price_drift = round(gamma * shares_per_trade + (rng.random() - 0.45) * 0.04, 4)
        curr_price = round(curr_price + price_drift, 4)
        trades.append((round(shares_per_trade, 2), curr_price))

    terminal_price = round(curr_price + ((seed * 5) % 11 - 5) * 0.03, 4)
    fees = round(10.0 + (seed % 25) * 1.5, 2)

    lambdas = [round(10.0 ** (-8.0 + 0.25 * i), 10) for i in range(21)]

    return {
        "seed": seed,
        "total_shares": total_shares,
        "horizon": horizon,
        "n_steps": n_steps,
        "daily_volume": daily_volume,
        "daily_volatility": daily_volatility,
        "gamma": gamma,
        "eta": eta,
        "risk_aversion": risk_aversion,
        "resilience": resilience,
        "decision_price": decision_price,
        "arrival_price": arrival_price,
        "terminal_price": terminal_price,
        "trades": trades,
        "fees": fees,
        "lambdas": lambdas,
    }
