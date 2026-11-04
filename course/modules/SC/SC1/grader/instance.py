"""Per-learner instances for the SC1 autograder of the reflection-principle engine. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws:

* a horizon H in 0.25 to 4.0 time units, rounded to three decimals, so H > 0;
* a level a in 0.25 to 2.5, rounded to three decimals, so a > 0;
* a grid size n_steps in 4 to 256 grid steps for the discrete maximum;
* a path count n_paths in 400 to 800, capped so that n_steps * n_paths <= 200000 generated increments.

The instance carries the seed and the label "SIMULATED". Nothing here is a real market, a real price or a real asset.
"""

from __future__ import annotations

import random
from typing import Any

_MAX_DRAWS = 200_000


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``. Every instance is valid under the project specification."""
    rng = random.Random(1_000_003 * int(seed) + 54_321)
    horizon = round(rng.uniform(0.25, 4.0), 3)
    level = round(rng.uniform(0.25, 2.5), 3)
    n_steps = rng.randint(4, 256)
    n_paths = rng.randint(400, min(800, _MAX_DRAWS // n_steps))
    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "H": horizon,
        "a": level,
        "n_steps": n_steps,
        "n_paths": n_paths,
    }
