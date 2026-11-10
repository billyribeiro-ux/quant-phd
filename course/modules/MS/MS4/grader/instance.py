"""Deterministic problem instance generator for MS4 Factor Strategy Capacity Study.

Exposes make_instance(seed: int) -> dict[str, object].
Generates synthetic equity universe parameters, trade targets, and market conditions.
"""

from __future__ import annotations

import random


def make_instance(seed: int) -> dict[str, object]:
    """Generate a deterministic test instance from an integer seed."""
    rng = random.Random(seed)

    n_assets = 50
    # Generate prices: $15.0 to $250.0
    prices = [round(rng.uniform(15.0, 250.0), 2) for _ in range(n_assets)]

    # Generate daily dollar volume ADV: $2M to $80M
    adv = [round(rng.uniform(2_000_000.0, 80_000_000.0), 2) for _ in range(n_assets)]

    # Generate daily return volatility: 1.2% to 3.8%
    sigma = [round(rng.uniform(0.012, 0.038), 5) for _ in range(n_assets)]

    # Select initial active holdings (15 assets)
    active_initial = rng.sample(range(n_assets), 15)
    raw_w_initial = [0.0] * n_assets
    for idx in active_initial:
        raw_w_initial[idx] = rng.uniform(0.5, 2.0)
    total_init = sum(raw_w_initial)
    w_initial = [round(w / total_init, 8) for w in raw_w_initial]
    w_initial[active_initial[0]] += 1.0 - sum(w_initial)  # exact normalization

    # Select target active holdings (15 assets with some overlap)
    active_target = rng.sample(range(n_assets), 15)
    raw_w_target = [0.0] * n_assets
    for idx in active_target:
        raw_w_target[idx] = rng.uniform(0.5, 2.0)
    total_target = sum(raw_w_target)
    w_target = [round(w / total_target, 8) for w in raw_w_target]
    w_target[active_target[0]] += 1.0 - sum(w_target)  # exact normalization

    # Strategy parameters
    gross_alpha = round(rng.uniform(0.06, 0.14), 4)  # 6% to 14% annualized gross alpha
    aum_test = round(rng.uniform(20_000_000.0, 300_000_000.0), 2)
    prefactor_y = 0.50

    # Ranks for buffer mitigation (permutation of 1..n_assets)
    shuffled_indices = list(range(n_assets))
    rng.shuffle(shuffled_indices)
    ranks = [0.0] * n_assets
    for rank, idx in enumerate(shuffled_indices, start=1):
        ranks[idx] = float(rank)

    target_n_assets = 15
    buffer_ratio = 1.5

    return {
        "seed": seed,
        "n_assets": n_assets,
        "prices": prices,
        "adv": adv,
        "sigma": sigma,
        "w_initial": w_initial,
        "w_target": w_target,
        "gross_alpha": gross_alpha,
        "aum_test": aum_test,
        "prefactor_y": prefactor_y,
        "ranks": ranks,
        "target_n_assets": target_n_assets,
        "buffer_ratio": buffer_ratio,
    }
