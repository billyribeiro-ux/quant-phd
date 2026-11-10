"""Per-learner instances for the BK1 project: ALM engine (alm.py).

make_instance(seed) is deterministic. It returns a SIMULATED bank balance sheet:
positions (parallel lists for cents, months where 0 marks non-rate-sensitive, and side),
non-maturity deposit book with deposit beta in basis points, base market rate in basis points,
a parallel rate shock in basis points, and a twist shock (short and long legs in basis points).

Every case is valid, and the seed changes the values across seeds.
Nothing here is market data or a real bank balance sheet.

alm.py never calls make_instance; a learner may call it only to inspect or test a case.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """A SIMULATED bank balance sheet and rate shock scenario for the given seed.

    Deterministic; every value is valid.
    """
    rng = random.Random(f"BK1-alm/{int(seed)}")

    # Balance sheet size scaling factor
    scale = rng.randint(50, 200)

    # Core rate-sensitive and non-rate-sensitive positions
    # 0 in position_months indicates non-rate-sensitive (months=None in Position)
    position_cents: list[int] = [
        rng.randint(20_000, 50_000) * scale,  # Cash & non-earning assets
        rng.randint(80_000, 150_000) * scale,  # Floating-rate loans (1 to 3m)
        rng.randint(100_000, 200_000) * scale,  # Medium-term loans (4 to 12m)
        rng.randint(250_000, 450_000) * scale,  # Long-term fixed mortgages (24 to 120m)
        rng.randint(60_000, 120_000) * scale,  # Short-term borrowings / CDs (1 to 6m)
        rng.randint(40_000, 100_000) * scale,  # Medium-to-long term debt (18 to 60m)
    ]
    position_months: list[int] = [
        0,  # non-rate-sensitive (corresponds to months=None)
        rng.randint(1, 3),
        rng.randint(4, 12),
        rng.choice([24, 36, 60, 84, 120]),
        rng.randint(1, 6),
        rng.choice([18, 36, 60]),
    ]
    position_sides: list[str] = [
        "asset",
        "asset",
        "asset",
        "asset",
        "liability",
        "liability",
    ]

    # Non-maturity core deposits (retail funding with partial interest rate pass-through)
    deposits_cents = rng.randint(300_000, 550_000) * scale
    beta_bp = rng.choice([1500, 2500, 3500, 4500, 6000, 7500])  # 15% to 75% pass-through

    base_rate_bp = rng.randint(200, 550)  # 2.00% to 5.50% base rate
    shock_bp = rng.choice([50, 100, 150, 200, 300])  # Parallel shift in bp

    # Yield curve twist: e.g. short rates rise faster than long rates (curve flattening or inversion)
    twist_short_bp = rng.randint(120, 280)
    twist_long_bp = rng.randint(20, 100)

    return {
        "seed": int(seed),
        "label": f"SIMULATED bank balance sheet, seed {int(seed)}: not market data",
        "position_cents": position_cents,
        "position_months": position_months,
        "position_sides": position_sides,
        "deposits_cents": deposits_cents,
        "beta_bp": beta_bp,
        "base_rate_bp": base_rate_bp,
        "shock_bp": shock_bp,
        "twist_short_bp": twist_short_bp,
        "twist_long_bp": twist_long_bp,
    }
