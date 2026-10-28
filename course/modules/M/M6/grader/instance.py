"""Per-learner instances for the M6 autograder: the martingale checks engine. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws:

* a horizon N in 4 to 10 steps of a fair walk, so that exact enumeration has at most 2**10 paths;
* a stopping rule tau = min(first time the walk reaches stop_level, stop_cap), with stop_level 1 or 2 and a cap
  stop_cap between 1 and N;
* a doubling case: a base stake s in 1 to 25 cents and a capital K = s * (2**J - 1) + e cents, with J in 1 to 8 and
  0 <= e < s * 2**J. With these values the strategy places exactly J bets when every bet loses, and K >= s;
* a dyadic level n in 3 to 10 and a barrier lambda in 1 to N for Doob's inequality.

Every instance uses a fair coin, win probability 1/2, so each walk is a martingale. The non-martingale control is
built by the grader from the same instance with win probability 1/3 and is not drawn here.

Nothing here is a real stake, a real market or a real price.
"""

from __future__ import annotations

import random
from fractions import Fraction
from typing import Any

_MAX_DOUBLINGS = 8


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``. Every instance is valid under the project specification."""
    rng = random.Random(1_000_003 * int(seed) + 12_345)
    horizon = rng.randint(4, 10)
    stop_level = rng.choice((1, 2))
    stop_cap = rng.randint(1, horizon)
    doublings = rng.randint(1, _MAX_DOUBLINGS)
    base = rng.randint(1, 25)
    extra = rng.randrange(0, base * 2**doublings)
    capital = base * (2**doublings - 1) + extra
    dyadic_level = rng.randint(3, 10)
    barrier = rng.randint(1, horizon)
    instance: dict[str, Any] = {
        "seed": int(seed),
        "label": "SIMULATED",
        "horizon": horizon,
        "win_probability": Fraction(1, 2),
        "stop_level": stop_level,
        "stop_cap": stop_cap,
        "capital_cents": capital,
        "base_stake_cents": base,
        "dyadic_level": dyadic_level,
        "barrier": barrier,
    }
    return instance
