"""Per-learner instances for the M5 autograder: the discounted Bellman operator on a finite grid.

All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws:

* a discount factor beta from 0.80 to 0.95 in steps of 0.01;
* a production exponent alpha from 0.30 to 0.70 in steps of 0.01;
* a strictly increasing grid of 8 to 24 capital values, whose first point lies in [0.20, 0.90] (so the first point is
  at most 1, which gives every state a feasible successor) and whose steps lie in [0.05, 0.40], with the last point
  above 1 so that some state cannot afford it;
* a stopping tolerance tol in {1e-6, 1e-8, 1e-10}.

A draw is rejected, and the next draw taken, when some grid point lies within 1e-6 of some resource level k**alpha.
Such a pair makes the feasibility test "k' <= k**alpha" a near-tie that floating point cannot settle the same way
in every correct implementation, so the contract would not then be a fair test of it.

Nothing here is a real economy, a real parameter or market data.
"""

from __future__ import annotations

import random
from typing import Any

_MARGIN = 1e-6
_TOLERANCES = (1e-6, 1e-8, 1e-10)


def _clear_of_ties(grid: list[float], alpha: float) -> bool:
    """True when no grid point lies within _MARGIN of a resource level k**alpha of any grid point k."""
    for k in grid:
        resources = k**alpha
        for point in grid:
            if abs(point - resources) <= _MARGIN:
                return False
    return True


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``: beta, alpha, a strictly increasing grid and tol."""
    for attempt in range(10_000):
        rng = random.Random(1_000_003 * int(seed) + 7_919 * attempt + 29)
        beta = rng.randrange(80, 96) / 100
        alpha = rng.randrange(30, 71) / 100
        size = rng.randrange(8, 25)
        first = rng.randrange(20, 91) / 100
        grid = [first]
        for _ in range(size - 1):
            grid.append(grid[-1] + rng.randrange(5, 41) / 100)
        if grid[-1] <= 1.0 or not _clear_of_ties(grid, alpha):
            continue
        tol = rng.choice(_TOLERANCES)
        return {
            "seed": int(seed),
            "label": "SIMULATED",
            "beta": beta,
            "alpha": alpha,
            "grid": grid,
            "tol": tol,
        }
    raise RuntimeError("no clear instance found in 10 000 draws")  # a guard against an endless loop
