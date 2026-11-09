"""Per-learner instances for the SC2 autograder of the Itô derivations engine. All values are SIMULATED.

``make_instance(seed)`` is deterministic and uses only the standard library. From the seed alone it draws:

* base GBM parameters s0 in [0.8, 1.5], mu in [-0.05, 0.10], sigma in [0.10, 0.40];
* base OU parameters x0 in [-0.3, 0.3], kappa in [0.5, 1.5], theta in [-0.2, 0.2];
* instance parameters r in [0.01, 0.05], p in {0.5, 2.0, 3.0}, a in [0.5, 2.0], b in [-1.5, -0.5] U [0.5, 1.5],
  c in [-0.5, 0.5], a0 in [0.01, 0.10], a1 in [0.005, 0.03];
* horizon H in [0.4, 0.8], bond maturity tbar in [H + 0.5, H + 1.5];
* grid size n_steps in 32 to 64, path count n_paths in 250 to 400.

The instance carries the seed and the label "SIMULATED". Nothing here is a real market, a real price or a real asset.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """A deterministic SIMULATED instance for ``seed``. Every instance is valid under the project specification."""
    rng = random.Random(2_000_003 * int(seed) + 76_543)
    s0 = round(rng.uniform(0.8, 1.5), 3)
    x0 = round(rng.uniform(-0.3, 0.3), 3)
    mu = round(rng.uniform(-0.05, 0.10), 3)
    sigma = round(rng.uniform(0.10, 0.40), 3)
    kappa = round(rng.uniform(0.5, 1.5), 3)
    theta = round(rng.uniform(-0.2, 0.2), 3)
    r = round(rng.uniform(0.01, 0.05), 3)
    p = rng.choice([0.5, 2.0, 3.0])
    a = round(rng.uniform(0.5, 2.0), 3)
    b_sign = rng.choice([-1.0, 1.0])
    b = round(b_sign * rng.uniform(0.5, 1.5), 3)
    c = round(rng.uniform(-0.5, 0.5), 3)
    a0 = round(rng.uniform(0.01, 0.10), 3)
    a1 = round(rng.uniform(0.005, 0.03), 3)
    horizon = round(rng.uniform(0.4, 0.8), 3)
    tbar = round(horizon + rng.uniform(0.5, 1.5), 3)
    n_steps = rng.randint(32, 64)
    n_paths = rng.randint(250, 400)
    return {
        "seed": int(seed),
        "label": "SIMULATED",
        "s0": s0,
        "x0": x0,
        "mu": mu,
        "sigma": sigma,
        "kappa": kappa,
        "theta": theta,
        "r": r,
        "p": p,
        "a": a,
        "b": b,
        "c": c,
        "a0": a0,
        "a1": a1,
        "H": horizon,
        "tbar": tbar,
        "n_steps": n_steps,
        "n_paths": n_paths,
    }
