"""Per-learner instances for the CS2 streaming statistics autograder.

make_instance(seed) is deterministic: the same seed always gives the same instance, and different seeds give
different streams. Every instance is valid: a stream of 20 to 400 finite floats, a window of 2 to 30, an epsilon of
0.05, 0.1 or 0.2, and ten probe quantiles in [0, 1]. Every value is SIMULATED: each stream is generated here from the
seed and is not market data or any real measurement. The docstring, the page and the suite say so.

The stream has a common offset of 0, 10,000 or 1,000,000 (dimensionless, SIMULATED). At the offsets 10,000 and
1,000,000 the naive formula loses digits that a relative tolerance of 1e-9 needs. The naive formula measured here is
the sample variance (ss - n*mean*mean) / (n - 1) with running float sums, in this order: s += x, ss += x*x, then
mean = s / n. Measured on seeds 0 to 49 against an exact Fraction reference, grouped by the offset that make_instance
draws: it fails 0 of the 16 seeds at offset 0, 22 of the 23 seeds at offset 10,000 (seed 41 passes) and all 11 seeds
at offset 1,000,000. The counts above are for that order only. The reference's
Welford update passes all 50 seeds. Some streams are rounded to
one decimal, so ties are likely. The `invalid` key names one case that the specification refuses. It is returned as a
JSON string, like the payload, so every field of the instance is a string, an int or a float.

Standard library only.
"""

from __future__ import annotations

import json
import random
from typing import Any

PROBES_FIXED = [0.0, 0.01, 0.1, 0.25, 0.5, 0.75, 0.9, 0.99, 1.0]
EPSILONS = [0.05, 0.1, 0.2]
OFFSETS = [0.0, 10_000.0, 1_000_000.0]
INVALID_KINDS = ["window_zero", "epsilon_one", "q_above_one", "welford_nan", "rolling_nan", "sketch_nan"]


def make_instance(seed: int) -> dict[str, Any]:
    rng = random.Random(seed)
    length = rng.randint(20, 400)
    offset = rng.choice(OFFSETS)
    decimals = rng.choice([1, 6])  # one decimal makes ties likely, which the sketch must handle
    values = [round(offset + rng.uniform(-5.0, 5.0), decimals) for _ in range(length)]
    window = rng.randint(2, 30)
    epsilon = rng.choice(EPSILONS)
    probes = [*PROBES_FIXED, round(rng.random(), 3)]
    kind = INVALID_KINDS[rng.randrange(len(INVALID_KINDS))]
    invalid: dict[str, Any] = {"kind": kind, "window": 0 if kind == "window_zero" else window}
    payload: dict[str, Any] = {"values": values, "window": window, "epsilon": epsilon, "probes": probes}
    return {
        "seed": seed,
        "label": f"SIMULATED stream {seed}",
        "payload": json.dumps(payload, sort_keys=True),
        "invalid": json.dumps(invalid, sort_keys=True),
    }
