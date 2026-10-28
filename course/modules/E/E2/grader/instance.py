"""Per-learner instances for the E2 autograder: a sealed-bid unit auction. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws:

* the bidder count ``n``, an integer from 2 to 5, and the unit count ``k``, an integer with ``1 <= k < n``;
* ``values``: ``n`` private values in integer cents, each from 0 to 10,000 inclusive (0.00 to 100.00);
* ``bids``: ``n`` bids in integer cents, each from 0 to 10,000 inclusive. The bids are drawn independently of the
  values, so a bid profile is not truthful and the efficiency test sees values and bids that differ.

Every instance is valid under the contract in project.html. Nothing here is a real auction, a real bidder or real
Treasury data.
"""

from __future__ import annotations

import random
from typing import Any

_MAX_CENTS = 10_000


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``: bidder count, unit count, private values and bids in cents."""
    rng = random.Random(int(seed))
    n = rng.randint(2, 5)
    k = rng.randint(1, n - 1)
    values = [rng.randint(0, _MAX_CENTS) for _ in range(n)]
    bids = [rng.randint(0, _MAX_CENTS) for _ in range(n)]
    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "n": n,
        "units": k,
        "values": values,
        "bids": bids,
    }
