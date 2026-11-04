"""Per-learner instances for the PC3 autograder: the fair-value path and the arrivals of one 20-turn market-making game.

All values are SIMULATED. Nothing here is market data.

``make_instance(seed)`` is deterministic and uses only the standard library. It draws from ``random.Random(seed)`` in a
fixed order, the same order as the seeded game of Lesson 4, so the seed-0 instance is the Lesson 4 game on seed 0:

* for each turn t = 1 .. 20, first one fair-value move: +5 cents when the draw is below 0.5, otherwise -5 cents;
* then one arrival: ``uninformed-buy`` when the draw is below 0.25, ``uninformed-sell`` when it is below 0.5, and
  ``informed`` otherwise.

The fair value starts at 10000 cents, so every fair value on the path is positive. Every instance this module returns is
therefore valid: it has 21 fair values, 20 arrivals, and only the three arrival names.
"""

from __future__ import annotations

import random
from typing import Any

HORIZON = 20  # turns
START_CENTS = 10_000  # v_0, in cents
MOVE_CENTS = 5  # the fair value moves by +5 or -5 cents each turn
ARRIVAL_NAMES = ("uninformed-buy", "uninformed-sell", "informed")


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``: the fair path v_0 .. v_20 (cents), the arrivals, the settlement.

    Keys: ``seed``, ``label`` (always "SIMULATED"), ``start_cents`` (10000), ``fair_path_cents`` (21 integers, v_0 to
    v_20), ``arrivals`` (20 names from ARRIVAL_NAMES, one per turn) and ``settlement_cents`` (v_20, in cents).
    """
    rng = random.Random(int(seed))
    path = [START_CENTS]
    arrivals: list[str] = []
    for _ in range(HORIZON):
        move = MOVE_CENTS if rng.random() < 0.5 else -MOVE_CENTS
        path.append(path[-1] + move)
        draw = rng.random()
        if draw < 0.25:
            arrivals.append("uninformed-buy")
        elif draw < 0.5:
            arrivals.append("uninformed-sell")
        else:
            arrivals.append("informed")
    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "start_cents": START_CENTS,
        "fair_path_cents": path,
        "arrivals": arrivals,
        "settlement_cents": path[HORIZON],
    }
