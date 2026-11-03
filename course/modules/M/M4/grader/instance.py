"""Per-learner instances for the M4 tail-risk simulator. Every value is SIMULATED: generated inputs, not market data.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws:

* two or three positions, each a whole number of cents from $1,000.00 to $50,000.00, all long;
* a return covariance matrix built as F F^T from a lower-triangular factor F with a diagonal from 0.01 to 0.04 and
  off-diagonal entries from -0.02 to 0.02, each factor entry rounded to 6 decimal places, and each entry of the
  product rounded to 12 decimal places, so the matrix is symmetric and positive definite by construction;
* a Student-t degrees-of-freedom nu in {3, 4, 5, 6, 7, 8}, so nu > 2 always;
* a number of draws from a fixed set, none of them a multiple of 100 (so the 99% order statistic is not an
  integer position), and none above 19,987.

Nothing here is a real portfolio, a real return or market data.
"""

from __future__ import annotations

import random
from typing import Any

_DRAWS = (6_003, 8_001, 9_997, 12_011, 15_013, 19_987)


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``. Every instance is valid under project.html."""
    rng = random.Random(7_919 * int(seed) + 104_729)
    n_assets = rng.choice((2, 3))
    positions = [rng.randrange(100_000, 5_000_001) for _ in range(n_assets)]
    factor = [[0.0] * n_assets for _ in range(n_assets)]
    for i in range(n_assets):
        for j in range(i):
            factor[i][j] = round(rng.uniform(-0.02, 0.02), 6)
        factor[i][i] = round(rng.uniform(0.01, 0.04), 6)
    cov = [
        [round(sum(factor[i][k] * factor[j][k] for k in range(n_assets)), 12) for j in range(n_assets)]
        for i in range(n_assets)
    ]
    nu = rng.randrange(3, 9)
    n_draws = rng.choice(_DRAWS)
    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "n_assets": n_assets,
        "positions_cents": positions,
        "cov": cov,
        "nu": nu,
        "n_draws": n_draws,
    }
