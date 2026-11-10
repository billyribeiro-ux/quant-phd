"""Instance generator for X4: Stablecoin Reserve Stress Test.

Generates deterministic problem instances covering reserve composition,
rate shocks, duration metrics, liquidation haircuts, and redemption stress grids.
"""

from __future__ import annotations

import random
from typing import Any

TIER_NAMES: list[str] = ["cash", "overnight_repo", "tbills_short", "treasury_notes", "bank_deposits"]


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic problem instance for seed."""
    rng = random.Random(seed)

    # Base liabilities: $10,000M to $50,000M ($10B to $50B)
    total_liabilities = round(10000.0 + (seed * 431) % 40000 + rng.uniform(0.0, 100.0), 2)

    # Surplus capital buffer: 0.2% to 1.2%
    surplus_pct = 0.002 + ((seed * 17) % 10) * 0.001
    total_assets = total_liabilities * (1.0 + surplus_pct)

    # Asset tier allocation weights (sum to 1.0)
    w_cash = 0.15 + (seed % 7) * 0.01  # 15% - 21%
    w_repo = 0.25 + ((seed * 3) % 8) * 0.01  # 25% - 32%
    w_tbills = 0.30 + ((seed * 5) % 6) * 0.01  # 30% - 35%
    w_bank = 0.08 + (seed % 5) * 0.01  # 8% - 12%
    w_notes = 1.0 - (w_cash + w_repo + w_tbills + w_bank)  # remaining ~10% - 20%

    # Durations
    d_tbills = round(0.20 + (seed % 5) * 0.03, 3)  # ~0.20 to ~0.32 yr
    d_notes = round(2.00 + ((seed * 7) % 7) * 0.20, 2)  # 2.0 to 3.2 yr

    # Haircuts
    h_repo = round(0.005 + (seed % 4) * 0.001, 4)
    h_tbills = round(0.010 + ((seed * 2) % 5) * 0.002, 4)
    h_notes = round(0.025 + ((seed * 3) % 4) * 0.005, 4)
    h_bank = round(0.060 + (seed % 5) * 0.010, 4)

    tier_pars = [
        round(total_assets * w_cash, 2),
        round(total_assets * w_repo, 2),
        round(total_assets * w_tbills, 2),
        round(total_assets * w_notes, 2),
        round(total_assets * w_bank, 2),
    ]
    tier_durations = [0.0, 0.0, d_tbills, d_notes, 0.0]
    tier_haircuts = [0.0, h_repo, h_tbills, h_notes, h_bank]

    rate_shock_bps = round(75.0 + (seed * 23) % 175, 1)  # 75 to 250 bps
    peg_threshold = 0.995 if seed % 2 == 0 else 0.990
    stressed_outflow_30d = round(total_liabilities * 0.30, 2)

    test_redemptions = [
        round(total_liabilities * 0.10, 2),
        round(total_liabilities * 0.25, 2),
        round(total_liabilities * 0.50, 2),
        round(total_liabilities * 0.75, 2),
    ]

    grid_shocks_bps = [0.0, 50.0, 100.0, 200.0, 300.0]
    grid_redemption_fractions = [0.10, 0.25, 0.50, 0.75]

    return {
        "seed": seed,
        "total_liabilities": total_liabilities,
        "tier_names": list(TIER_NAMES),
        "tier_pars": tier_pars,
        "tier_durations": tier_durations,
        "tier_haircuts": tier_haircuts,
        "rate_shock_bps": rate_shock_bps,
        "peg_threshold": peg_threshold,
        "stressed_outflow_30d": stressed_outflow_30d,
        "test_redemptions": test_redemptions,
        "grid_shocks_bps": grid_shocks_bps,
        "grid_redemption_fractions": grid_redemption_fractions,
    }


def get_reserve_assets(inst: dict[str, Any]) -> dict[str, dict[str, float]]:
    """Reconstruct tiered reserve assets dictionary from instance arrays."""
    names: list[str] = inst["tier_names"]
    pars: list[float] = inst["tier_pars"]
    durations: list[float] = inst["tier_durations"]
    haircuts: list[float] = inst["tier_haircuts"]

    return {
        name: {"par": p, "duration": d, "haircut": h}
        for name, p, d, h in zip(names, pars, durations, haircuts, strict=True)
    }
