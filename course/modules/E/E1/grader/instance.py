"""Per-learner instances for the E1 market-structure engine (market_structure.py).

make_instance(seed) is deterministic. It returns a SIMULATED case: generated integers for a two-exchange trade market,
not data from any exchange. The three integers are the inputs of the project specification:

* ``a``, trades at a fee of zero, a whole number of trades;
* ``b``, trades per (cent per trade) that the fee removes, a whole number of trades per (cent per trade), from 1 to 3;
* ``c``, the constant cost of one trade to the exchange, in cents per trade, from 5 to 60.

The generator draws b and c, then a gap d = a - b*c in trades, from 60 to 400. The gap is above 6*b, so every fee and
volume that the specification compares differs by more than one unit, and the rounded orderings of the outputs are
strict on every seed. Every case is valid: a > b*c > 0. The seed draws b, c and the gap, so the volumes, fees and
surpluses differ across seeds.
"""

from __future__ import annotations

import random


def make_instance(seed: int) -> dict[str, int]:
    rng = random.Random(f"E1-market-structure/{int(seed)}")
    b = rng.randint(1, 3)
    c = rng.randint(5, 60)
    gap = rng.randint(60, 400)  # d = a - b c, in trades; above 6 b on every seed
    a = b * c + gap
    return {"a": a, "b": b, "c": c}
