"""Per-learner instances for the FC1 project: the cash-instrument engine (instruments.py).

make_instance(seed) is deterministic. It returns a SIMULATED case: one fixed-rate bond (a whole-cent face, a coupon in
basis points of face per period, a number of periods and a per-period yield in basis points) and one cash trade (a
quantity of units, a price in cents per unit, a side and a settlement period). Every case is valid, and the seed
changes the answers. Nothing here is market data or a real security.

The project page states the conventions these values follow: rates in basis points, money in whole cents, periods
as whole numbers from 1. instruments.py never calls make_instance; a learner may call it only to read a case.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """A SIMULATED bond and trade for the given seed. Deterministic; every value is valid."""
    rng = random.Random(f"FC1-cash-engine/{int(seed)}")
    face_cents = rng.randint(100_000, 5_000_000)  # a face of 1,000.00 to 50,000.00 in cents, not always a round amount
    coupon_bps = rng.randint(100, 900)  # the coupon per period, in basis points of face
    periods = rng.randint(1, 8)  # coupon periods, numbered 1 to periods
    yield_bps = rng.randint(50, 900)  # the per-period yield, in basis points
    quantity = rng.randint(1, 500)  # units of the cash instrument in the trade
    price_cents = rng.randint(5_000, 150_000)  # cents per unit
    side = rng.choice((1, -1))  # +1 buys (the holder pays cash), -1 sells (the holder receives cash)
    settlement_day = rng.randint(1, 5)  # the period in which the trade settles, numbered from 1
    return {
        "seed": int(seed),
        "label": f"SIMULATED bond and trade, seed {int(seed)}: not market data",
        "face_cents": face_cents,
        "coupon_bps": coupon_bps,
        "periods": periods,
        "yield_bps": yield_bps,
        "quantity": quantity,
        "price_cents": price_cents,
        "side": side,
        "settlement_day": settlement_day,
    }
