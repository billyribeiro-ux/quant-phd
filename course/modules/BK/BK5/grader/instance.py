"""Per-learner instances for the BK5 project: retirement planning and wealth management engine.

make_instance(seed) is deterministic. It returns a SIMULATED household planning profile:
- 25-year projected annual labor earnings (integer cents) and a human capital discount rate in basis points;
- Target dollar allocations to equities and fixed income (integer cents);
- Account capacities across Taxable, Traditional (TDA), and Roth accounts (integer cents);
- A 50-year historical annual real return series (floats) calibrated to historical equity/bond performance;
- Moving-block bootstrap parameters (block length, 30-year retirement horizon, simulation count);
- Decumulation parameters (initial retirement wealth, initial withdrawal rate in basis points, max ruin tolerance).

All values are SIMULATED and deterministic.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic household wealth management instance for the given seed."""
    rng = random.Random(f"BK5-retirement-plan/{int(seed)}")

    # 1. Human capital parameters
    working_years = 25
    base_salary_cents = rng.randint(8_000_000, 15_000_000)  # $80,000 to $150,000
    growth_rate = rng.choice([0.01, 0.015, 0.02, 0.025])
    earnings_cents: list[int] = []
    curr_salary = float(base_salary_cents)
    for _ in range(working_years):
        earnings_cents.append(round(curr_salary))
        curr_salary *= 1.0 + growth_rate

    discount_rate_bps = rng.choice([300, 350, 400, 450])  # 3.0% to 4.5%

    # 2. Asset location parameters
    # Total portfolio between $500,000 and $2,000,000
    total_wealth_cents = rng.randint(50_000_000, 200_000_000)
    # Ensure total wealth is a clean round number divisible by 100_000
    total_wealth_cents = (total_wealth_cents // 100_000) * 100_000

    equity_share = rng.choice([0.50, 0.60, 0.70])
    equity_target_cents = round(total_wealth_cents * equity_share)
    bond_target_cents = total_wealth_cents - equity_target_cents

    # Account capacity splits
    # Taxable ~ 40%, TDA ~ 40%, Roth ~ 20%
    taxable_pct = rng.choice([0.35, 0.40, 0.45])
    roth_pct = rng.choice([0.15, 0.20, 0.25])
    round(1.0 - taxable_pct - roth_pct, 4)

    taxable_capacity_cents = round(total_wealth_cents * taxable_pct)
    roth_capacity_cents = round(total_wealth_cents * roth_pct)
    tda_capacity_cents = total_wealth_cents - taxable_capacity_cents - roth_capacity_cents

    # 3. Historical return series for moving-block bootstrap
    # 50 annual real returns calibrated with mean 0.055, vol 0.12, AR(1) persistence 0.15
    hist_len = 50
    historical_returns: list[float] = []
    prev_ret = 0.055
    for _ in range(hist_len):
        shock = rng.gauss(0.0, 0.11)
        ret = 0.055 + 0.15 * (prev_ret - 0.055) + shock
        # Bound returns within plausible historical range [-0.35, +0.45]
        ret = max(-0.35, min(0.45, round(ret, 4)))
        historical_returns.append(ret)
        prev_ret = ret

    block_length = rng.choice([3, 4, 5])
    horizon_years = 30
    n_simulations = 200  # fast and deterministic

    # 4. Decumulation parameters
    initial_withdrawal_bps = rng.choice([350, 400, 450, 500])  # 3.5% to 5.0%
    max_ruin_prob = rng.choice([0.05, 0.10])

    return {
        "seed": int(seed),
        "label": f"SIMULATED household profile, seed {int(seed)}: not market data",
        "earnings_cents": earnings_cents,
        "discount_rate_bps": discount_rate_bps,
        "total_wealth_cents": total_wealth_cents,
        "equity_target_cents": equity_target_cents,
        "bond_target_cents": bond_target_cents,
        "taxable_capacity_cents": taxable_capacity_cents,
        "tda_capacity_cents": tda_capacity_cents,
        "roth_capacity_cents": roth_capacity_cents,
        "historical_returns": historical_returns,
        "block_length": block_length,
        "horizon_years": horizon_years,
        "n_simulations": n_simulations,
        "initial_withdrawal_bps": initial_withdrawal_bps,
        "max_ruin_prob": max_ruin_prob,
    }
