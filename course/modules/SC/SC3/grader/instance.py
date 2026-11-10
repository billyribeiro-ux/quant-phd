"""Instance generator for SC3: Numeraire Toolkit.

Generates deterministic, parameterized market specifications for two correlated assets
and cross-currency quanto parameters under simulated continuous-time dynamics.
All instances are labeled SIMULATED.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Return a deterministic market instance for the given integer seed."""
    rng = random.Random(seed)

    # Correlated asset parameters for exchange option (Margrabe)
    s1 = round(80.0 + rng.random() * 40.0, 3)
    s2 = round(80.0 + rng.random() * 40.0, 3)
    sig1 = round(0.15 + rng.random() * 0.20, 3)
    sig2 = round(0.15 + rng.random() * 0.20, 3)
    rho = round(-0.60 + rng.random() * 1.20, 3)
    q1 = round(0.01 + rng.random() * 0.04, 3)
    q2 = round(0.01 + rng.random() * 0.04, 3)
    t = round(0.5 + rng.random() * 1.5, 3)
    r = round(0.02 + rng.random() * 0.04, 3)

    # Quanto contract parameters
    s_f = round(90.0 + rng.random() * 30.0, 3)
    x0 = round(1.10 + rng.random() * 0.30, 3)
    k_quanto = round(85.0 + rng.random() * 30.0, 3)
    r_d = round(0.03 + rng.random() * 0.03, 3)
    r_f = round(0.01 + rng.random() * 0.03, 3)
    sig_s = round(0.18 + rng.random() * 0.15, 3)
    sig_x = round(0.10 + rng.random() * 0.10, 3)
    rho_sx = round(-0.50 + rng.random() * 1.00, 3)
    n_paths = 5000

    return {
        "s1": s1,
        "s2": s2,
        "sig1": sig1,
        "sig2": sig2,
        "rho": rho,
        "q1": q1,
        "q2": q2,
        "t": t,
        "r": r,
        "s_f": s_f,
        "x0": x0,
        "k_quanto": k_quanto,
        "r_d": r_d,
        "r_f": r_f,
        "sig_s": sig_s,
        "sig_x": sig_x,
        "rho_sx": rho_sx,
        "n_paths": n_paths,
        "seed": seed,
    }
