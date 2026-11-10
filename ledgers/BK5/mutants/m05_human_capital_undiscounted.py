"""Student error: calculates human capital as undiscounted sum of earnings, ignoring time value of money.

Standard library only. Integer cents for all monetary quantities.
"""

from __future__ import annotations

import random
from typing import Any


def human_capital_value(earnings_cents: list[int], discount_rate_bps: int) -> int:
    if not earnings_cents or any(e < 0 for e in earnings_cents) or discount_rate_bps < 0:
        raise ValueError("invalid")
    # ERROR: undiscounted sum, ignoring discount_rate_bps
    return sum(earnings_cents)


def optimal_asset_location(
    equity_target_cents: int,
    bond_target_cents: int,
    taxable_capacity_cents: int,
    tda_capacity_cents: int,
    roth_capacity_cents: int,
) -> dict[str, dict[str, int]]:
    inputs = [equity_target_cents, bond_target_cents, taxable_capacity_cents, tda_capacity_cents, roth_capacity_cents]
    if any(x < 0 for x in inputs) or sum(inputs[:2]) != sum(inputs[2:]):
        raise ValueError("invalid")
    tda_bond = min(bond_target_cents, tda_capacity_cents)
    rem_bond = bond_target_cents - tda_bond
    taxable_bond = min(rem_bond, taxable_capacity_cents)
    roth_bond = rem_bond - taxable_bond
    return {
        "taxable": {"equity": taxable_capacity_cents - taxable_bond, "bond": taxable_bond},
        "tda": {"equity": tda_capacity_cents - tda_bond, "bond": tda_bond},
        "roth": {"equity": roth_capacity_cents - roth_bond, "bond": roth_bond},
    }


def moving_block_bootstrap(
    returns: list[float],
    block_length: int,
    horizon: int,
    n_paths: int,
    seed: int,
) -> list[list[float]]:
    n = len(returns)
    if n == 0 or block_length < 1 or block_length > n or horizon < 1 or n_paths < 1:
        raise ValueError("invalid")
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
    if initial_wealth_cents <= 0 or initial_withdrawal_bps <= 0 or not return_paths:
        raise ValueError("invalid")
    withdrawal_cents = (initial_wealth_cents * initial_withdrawal_bps) // 10_000
    n_paths = len(return_paths)
    ruin_count = 0
    terminal_wealths: list[int] = []
    for path in return_paths:
        w = float(initial_wealth_cents)
        ruined = False
        for r in path:
            w -= withdrawal_cents
            if w <= 0.0:
                ruined = True
                w = 0.0
                break
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
    median_tw = (
        sorted_tw[n_paths // 2] if n_paths % 2 == 1 else (sorted_tw[n_paths // 2 - 1] + sorted_tw[n_paths // 2]) // 2
    )
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
    if max_ruin_prob < 0.0 or max_ruin_prob > 1.0 or step_bps < 1:
        raise ValueError("invalid")
    best_rate = 0
    current_rate = 100
    while current_rate <= 1000:
        sim = simulate_withdrawals(initial_wealth_cents, current_rate, return_paths)
        if sim["ruin_probability"] <= max_ruin_prob:
            best_rate = current_rate
        else:
            break
        current_rate += step_bps
    return best_rate
