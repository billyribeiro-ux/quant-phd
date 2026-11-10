"""Reference solution for the BK5 retirement planning engine (retirement_plan.py).

Standard library only. Integer cents for all monetary quantities.
Deterministic moving-block bootstrap and decumulation simulation.
"""

from __future__ import annotations

import random
from typing import Any


def human_capital_value(earnings_cents: list[int], discount_rate_bps: int) -> int:
    """Calculate the present value of projected labor earnings in integer cents.

    earnings_cents: list of annual projected earnings in integer cents.
    discount_rate_bps: discount rate in basis points (e.g., 350 for 3.50%).
    Raises ValueError on negative earnings, empty list, or negative discount rate.
    """
    if not earnings_cents:
        raise ValueError("earnings_cents cannot be empty")
    if any(e < 0 for e in earnings_cents):
        raise ValueError("earnings cannot be negative")
    if discount_rate_bps < 0:
        raise ValueError("discount_rate_bps cannot be negative")

    r = discount_rate_bps / 10_000.0
    pv_total = 0.0
    for t, earnings in enumerate(earnings_cents, start=1):
        pv_total += earnings / ((1.0 + r) ** t)

    return round(pv_total)


def optimal_asset_location(
    equity_target_cents: int,
    bond_target_cents: int,
    taxable_capacity_cents: int,
    tda_capacity_cents: int,
    roth_capacity_cents: int,
) -> dict[str, dict[str, int]]:
    """Allocate equity and bond targets across Taxable, TDA, and Roth accounts to maximize tax efficiency.

    Tax-efficiency hierarchy:
    1. Bonds placed in TDA first to shield ordinary income from annual taxation.
    2. Any remaining bonds placed in Taxable.
    3. Equities fill remaining capacities: Roth first (maximizing tax-free compounding of growth),
       then Taxable, then TDA.
    Conservation: account allocations exactly equal targets and capacities.
    Raises ValueError on negative inputs or if targets sum != capacities sum.
    """
    inputs = [
        equity_target_cents,
        bond_target_cents,
        taxable_capacity_cents,
        tda_capacity_cents,
        roth_capacity_cents,
    ]
    if any(x < 0 for x in inputs):
        raise ValueError("targets and capacities cannot be negative")

    total_target = equity_target_cents + bond_target_cents
    total_capacity = taxable_capacity_cents + tda_capacity_cents + roth_capacity_cents
    if total_target != total_capacity:
        raise ValueError(f"targets sum ({total_target}) does not match capacities sum ({total_capacity})")

    # Step 1: Bonds to TDA
    tda_bond = min(bond_target_cents, tda_capacity_cents)
    remaining_bond = bond_target_cents - tda_bond

    # Step 2: Bonds to Taxable if TDA full
    taxable_bond = min(remaining_bond, taxable_capacity_cents)
    remaining_bond -= taxable_bond

    # Step 3: Extreme case - bonds to Roth if both TDA and Taxable full
    roth_bond = remaining_bond

    # Step 4: Equities fill remaining capacities
    tda_equity = tda_capacity_cents - tda_bond
    taxable_equity = taxable_capacity_cents - taxable_bond
    roth_equity = roth_capacity_cents - roth_bond

    return {
        "taxable": {"equity": taxable_equity, "bond": taxable_bond},
        "tda": {"equity": tda_equity, "bond": tda_bond},
        "roth": {"equity": roth_equity, "bond": roth_bond},
    }


def moving_block_bootstrap(
    returns: list[float],
    block_length: int,
    horizon: int,
    n_paths: int,
    seed: int,
) -> list[list[float]]:
    """Generate synthetic return paths via moving-block bootstrap with replacement.

    returns: 1D historical series of length N.
    block_length: length b of each block (1 <= b <= N).
    horizon: length H of each generated synthetic path.
    n_paths: number of synthetic paths to generate.
    seed: RNG seed for determinism.
    """
    n = len(returns)
    if n == 0:
        raise ValueError("returns series cannot be empty")
    if block_length < 1 or block_length > n:
        raise ValueError(f"block_length must be between 1 and {n}")
    if horizon < 1:
        raise ValueError("horizon must be at least 1")
    if n_paths < 1:
        raise ValueError("n_paths must be at least 1")

    num_blocks = n - block_length + 1
    rng = random.Random(seed)
    paths: list[list[float]] = []

    for _ in range(n_paths):
        path: list[float] = []
        while len(path) < horizon:
            start_idx = rng.randint(0, num_blocks - 1)
            path.extend(returns[start_idx : start_idx + block_length])
        paths.append(path[:horizon])

    return paths


def simulate_withdrawals(
    initial_wealth_cents: int,
    initial_withdrawal_bps: int,
    return_paths: list[list[float]],
) -> dict[str, Any]:
    """Simulate annual retirement decumulation under constant real withdrawals.

    Withdrawal occurs at the beginning of each year.
    If portfolio wealth drops <= 0, the path is ruined (terminal wealth = 0).
    Returns ruin_probability, terminal_wealths_cents, and median_terminal_wealth_cents.
    """
    if initial_wealth_cents <= 0:
        raise ValueError("initial_wealth_cents must be positive")
    if initial_withdrawal_bps <= 0:
        raise ValueError("initial_withdrawal_bps must be positive")
    if not return_paths:
        raise ValueError("return_paths cannot be empty")

    withdrawal_cents = (initial_wealth_cents * initial_withdrawal_bps) // 10_000
    n_paths = len(return_paths)
    ruin_count = 0
    terminal_wealths: list[int] = []

    for path in return_paths:
        w = float(initial_wealth_cents)
        ruined = False
        for r in path:
            # Beginning-of-year withdrawal
            w -= withdrawal_cents
            if w <= 0.0:
                ruined = True
                w = 0.0
                break
            # Investment return during year
            w *= 1.0 + r
            if w <= 0.0:
                ruined = True
                w = 0.0
                break

        if ruined:
            ruin_count += 1
            terminal_wealths.append(0)
        else:
            terminal_wealths.append(round(w))

    ruin_prob = round(ruin_count / n_paths, 4)

    sorted_tw = sorted(terminal_wealths)
    if n_paths % 2 == 1:
        median_tw = sorted_tw[n_paths // 2]
    else:
        median_tw = (sorted_tw[n_paths // 2 - 1] + sorted_tw[n_paths // 2]) // 2

    return {
        "ruin_probability": ruin_prob,
        "terminal_wealths_cents": terminal_wealths,
        "median_terminal_wealth_cents": median_tw,
    }


def safe_withdrawal_rate(
    initial_wealth_cents: int,
    return_paths: list[list[float]],
    max_ruin_prob: float = 0.05,
    step_bps: int = 5,
) -> int:
    """Find the maximum initial withdrawal rate in bps whose ruin probability <= max_ruin_prob.

    Searches rates from 100 bps (1%) to 1000 bps (10%) in increments of step_bps.
    Returns the rate in bps, or 0 if no rate satisfies the threshold.
    """
    if max_ruin_prob < 0.0 or max_ruin_prob > 1.0:
        raise ValueError("max_ruin_prob must be between 0.0 and 1.0")
    if step_bps < 1:
        raise ValueError("step_bps must be at least 1")

    best_rate = 0
    current_rate = 100
    while current_rate <= 1000:
        sim = simulate_withdrawals(initial_wealth_cents, current_rate, return_paths)
        if sim["ruin_probability"] <= max_ruin_prob:
            best_rate = current_rate
        else:
            # Ruin probability is non-decreasing in withdrawal rate
            break
        current_rate += step_bps

    return best_rate
