"""Instance generator for PR1 autograded project.

SIMULATED: generated inputs, not market data.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic multi-asset investment instance.

    Parameters
    ----------
    seed : int
        Pseudorandom seed (determines asset universe and return series).

    Returns
    -------
    dict[str, Any]
        Dictionary containing names, returns, window, gamma, delta, tau,
        w_mkt, P, q, omega, and cost_rate.
    """
    rng = random.Random(seed)
    n = 4 + (seed % 3)  # Universe size N in {4, 5, 6}
    h = 120  # Total periods H
    window = 60  # Estimation window T = 60 (rebalances K = 60)
    gamma = 2.0 + (seed % 4) * 0.8
    delta = 0.25 + (seed % 5) * 0.12
    tau = 0.03 + (seed % 4) * 0.02
    cost_rates = [0.0005, 0.001, 0.002]
    cost_rate = cost_rates[seed % len(cost_rates)]
    names = [f"Asset_{chr(65 + i)}" for i in range(n)]

    # Market capitalization weights (positive, sum to 1.0)
    raw_mkt = [1.0 + rng.random() for _ in range(n)]
    tot_mkt = sum(raw_mkt)
    w_mkt = [round(x / tot_mkt, 6) for x in raw_mkt]
    w_mkt[0] += round(1.0 - sum(w_mkt), 6)  # exact normalization

    # Multi-factor return generation to ensure full rank and realistic correlations
    drift = [0.004 + 0.008 * rng.random() for _ in range(n)]
    vol = [0.03 + 0.02 * rng.random() for _ in range(n)]
    beta1 = [0.6 + 0.8 * rng.random() for _ in range(n)]
    beta2 = [-0.3 + 0.6 * rng.random() for _ in range(n)]

    returns: list[list[float]] = []
    for _ in range(h):
        f1 = rng.gauss(0.0, 0.04)
        f2 = rng.gauss(0.0, 0.03)
        row: list[float] = []
        for i in range(n):
            idio = rng.gauss(0.0, vol[i])
            r = drift[i] + beta1[i] * f1 + beta2[i] * f2 + idio
            row.append(round(r, 6))
        returns.append(row)

    # Investor views for Black-Litterman
    if seed % 2 == 0:
        # One relative view: Asset A outperforms Asset B
        p = [[0.0] * n]
        p[0][0] = 1.0
        p[0][1] = -1.0
        q = [round(0.005 + 0.005 * rng.random(), 5)]
        omega = [round(0.0004 + 0.0002 * rng.random(), 6)]
    else:
        # Two views: one relative, one absolute
        p = [[0.0] * n, [0.0] * n]
        p[0][0] = 1.0
        p[0][1] = -1.0
        p[1][2] = 1.0
        q = [
            round(0.004 + 0.004 * rng.random(), 5),
            round(0.008 + 0.004 * rng.random(), 5),
        ]
        omega = [
            round(0.0003 + 0.0001 * rng.random(), 6),
            round(0.0005 + 0.0002 * rng.random(), 6),
        ]

    return {
        "names": names,
        "returns": returns,
        "window": window,
        "gamma": gamma,
        "delta": delta,
        "tau": tau,
        "w_mkt": w_mkt,
        "P": p,
        "q": q,
        "omega": omega,
        "cost_rate": cost_rate,
    }
