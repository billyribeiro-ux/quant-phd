"""Deterministic project instance generator for CF6: Raising Capital & Investment Banking.

Exposes make_instance(seed: int) -> dict[str, Any].
Standard library only, fully deterministic across seeds.
"""

from __future__ import annotations

import json
import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic, valid project instance for the given seed."""
    rng = random.Random(seed)

    # 1. Rock (1986) Winner's Curse parameters
    v_low = round(rng.uniform(10.0, 16.0), 2)
    v_high = round(rng.uniform(24.0, 36.0), 2)
    prob_high = round(rng.uniform(0.45, 0.70), 2)
    s_shares = rng.randint(1_000, 3_000) * 1_000  # 1M to 3M shares
    informed_demand = rng.randint(1_200, 3_500) * 1_000
    uninformed_budget = round(rng.uniform(35_000_000.0, 75_000_000.0), 2)

    # 2. Bookbuilding bids (8 syndicate & investor participants)
    base_price = round(rng.uniform(18.0, 24.0), 2)
    clearing_price = base_price
    total_shares_offered = rng.randint(2_000, 4_000) * 1_000

    bids: list[dict[str, Any]] = []
    # Institutional bids (informed or large)
    info_states = ["positive", "neutral", "negative"]
    for i in range(1, 6):
        b_price = round(clearing_price + rng.choice([-2.0, -1.0, 0.0, 1.0, 2.0, 3.0]), 2)
        b_shares = rng.randint(400, 1_200) * 1_000
        b_info = rng.choice(info_states)
        bids.append(
            {
                "bidder_id": f"inst_{i:02d}",
                "bid_price": b_price,
                "bid_shares": b_shares,
                "revealed_info": b_info,
                "investor_type": "institutional",
            }
        )
    # Retail bids (uninformed)
    for j in range(1, 4):
        b_price = round(clearing_price + rng.choice([-1.5, 0.0, 0.5, 1.5]), 2)
        b_shares = rng.randint(150, 450) * 1_000
        bids.append(
            {
                "bidder_id": f"retail_{j:02d}",
                "bid_price": b_price,
                "bid_shares": b_shares,
                "revealed_info": "neutral",
                "investor_type": "retail",
            }
        )

    # 3. Myers & Majluf (1984) SEO parameters
    v_assets_good = round(rng.uniform(180.0, 260.0), 2)
    v_assets_bad = round(rng.uniform(70.0, 120.0), 2)
    prob_good = round(rng.uniform(0.40, 0.60), 2)
    project_cost = round(rng.uniform(30.0, 60.0), 2)
    project_npv = round(rng.uniform(6.0, 18.0), 2)
    slack_cash = round(rng.uniform(5.0, 15.0), 2)

    # 4. Long-run abnormal returns (36 monthly periods)
    # Simulate IPO underperformance: IPO mean ~0.7% monthly vs benchmark mean ~1.2% monthly
    firm_returns = [round(rng.gauss(0.007, 0.06), 4) for _ in range(36)]
    benchmark_returns = [round(rng.gauss(0.012, 0.04), 4) for _ in range(36)]

    # 5. Syndicate economics (gross spread, 7% clustering)
    gross_proceeds_millions = rng.randint(60, 200)
    gross_proceeds_cents = gross_proceeds_millions * 100_000_000
    spread_bps = 700  # Classic 7% gross spread
    lead_manager_share = 0.60
    co_manager_share = 0.30
    selling_group_share = 0.10

    return {
        "v_low": v_low,
        "v_high": v_high,
        "prob_high": prob_high,
        "s_shares": s_shares,
        "informed_demand": informed_demand,
        "uninformed_budget": uninformed_budget,
        "bids_json": json.dumps(bids),
        "total_shares_offered": total_shares_offered,
        "clearing_price": clearing_price,
        "v_assets_good": v_assets_good,
        "v_assets_bad": v_assets_bad,
        "prob_good": prob_good,
        "project_cost": project_cost,
        "project_npv": project_npv,
        "slack_cash": slack_cash,
        "firm_returns": firm_returns,
        "benchmark_returns": benchmark_returns,
        "gross_proceeds_cents": gross_proceeds_cents,
        "spread_bps": spread_bps,
        "lead_manager_share": lead_manager_share,
        "co_manager_share": co_manager_share,
        "selling_group_share": selling_group_share,
    }
