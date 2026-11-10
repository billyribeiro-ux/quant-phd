"""Per-learner instances for the BK3 project: the LDI collateral-spiral simulator (ldi_model.py).

make_instance(seed: int) -> dict[str, Any] is deterministic and returns a SIMULATED leveraged LDI pension fund:
assets, asset duration, overlay notional, overlay duration, liquid cash buffer, price-impact coefficient,
central-bank backstop trigger and capacity, and an initial yield shock.

All monetary amounts are integer cents, durations are in hundredths of a year (e.g. 1500 = 15.00y),
and yield moves / impacts are in basis points.
Every case is valid, and the seed changes the answers across seeds 0-49. Nothing here is real market data.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """A SIMULATED leveraged LDI fund and shock for the given seed. Deterministic; every value is valid."""
    rng = random.Random(f"BK3-ldi-spiral/{int(seed)}")
    assets = rng.randint(500_000_000, 2_000_000_000)  # 5M to 20M USD in cents
    asset_duration_cy = rng.randint(600, 1500)  # 6.00y to 15.00y
    overlay_notional = rng.randint(200_000_000, 800_000_000)  # 2M to 8M USD notional
    overlay_duration_cy = rng.randint(1000, 2500)  # 10.00y to 25.00y
    buffer = rng.randint(5_000_000, 30_000_000)  # 50k to 300k USD buffer
    impact = rng.randint(500, 2500)  # 500 to 2500 bps per 10^9 cents sold
    backstop_trigger = rng.randint(40, 120)  # 40 to 120 bps trigger
    backstop_capacity = rng.randint(15_000_000, 60_000_000)  # backstop capacity in cents

    # Closed-form threshold: ceil((2*B + 1) * 10^6 / (2 * N * D_h))
    num = (2 * buffer + 1) * 1_000_000
    den = 2 * overlay_notional * overlay_duration_cy
    thresh = -(-num // den)
    # Ensure initial shock reaches forced sales to exercise the spiral
    shock = thresh + rng.randint(5, 35)

    return {
        "seed": int(seed),
        "label": f"SIMULATED LDI fund, seed {int(seed)}: illustrative parameters, not market data",
        "assets_cents": assets,
        "asset_duration_cy": asset_duration_cy,
        "overlay_notional_cents": overlay_notional,
        "overlay_duration_cy": overlay_duration_cy,
        "buffer_cents": buffer,
        "impact_bps_per_gcent": impact,
        "backstop_trigger_bps": backstop_trigger,
        "backstop_capacity_cents": backstop_capacity,
        "shock_bps": shock,
        "threshold_bps": thresh,
    }
