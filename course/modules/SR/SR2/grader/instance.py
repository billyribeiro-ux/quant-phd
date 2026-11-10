"""Deterministic problem instance generator for SR2: Leverage-cycle model.

Generates reproducible problem instances for the autograder.
"""

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic test instance for a given seed.

    Parameters
    ----------
    seed : int
        RNG seed.

    Returns
    -------
    dict[str, Any]
        Dictionary of parameters for two-state equilibrium, margin shocks,
        and three-period leverage cycle.
    """
    rng = random.Random(seed)

    v_d = round(rng.uniform(0.20, 0.80), 4)
    v_u = round(v_d + rng.uniform(0.40, 1.50), 4)
    rf = round(rng.uniform(1.0, 1.08), 4)

    initial_loan_ratio = round(rng.uniform(0.80, 1.0), 4)
    shocked_loan_ratio = round(rng.uniform(0.25, 0.65), 4)

    # Payoffs for three-period tree
    v_dd = round(rng.uniform(0.10, 0.35), 4)
    v_du = round(v_dd + rng.uniform(0.30, 0.60), 4)
    v_ud = round(v_du + rng.uniform(0.20, 0.50), 4)
    v_uu = round(v_ud + rng.uniform(0.50, 1.20), 4)

    return {
        "v_u": v_u,
        "v_d": v_d,
        "risk_free_rate": rf,
        "initial_loan_ratio": initial_loan_ratio,
        "shocked_loan_ratio": shocked_loan_ratio,
        "v_uu": v_uu,
        "v_ud": v_ud,
        "v_du": v_du,
        "v_dd": v_dd,
    }
