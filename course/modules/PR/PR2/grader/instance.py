"""Instance generator for PR2 autograded project (Atlas A11).

SIMULATED: generates synthetic asset return histories and investment parameters
for seed-specific portfolio construction tests.
"""

from __future__ import annotations

import random
from typing import Any


def make_instance(seed: int) -> dict[str, Any]:
    """Generate a deterministic multi-asset investment instance for Atlas A11.

    Parameters
    ----------
    seed : int
        Seed for the pseudorandom number generator.

    Returns
    -------
    dict[str, Any]
        Dictionary containing asset names, return history matrix, expected
        returns, target volatility, risk budgets, risk aversion, and leverage cap.
    """
    rng = random.Random(seed)
    n = 4 + (seed % 3)  # 4, 5, or 6 assets
    t = 120  # 120 historical observation periods (e.g. 10 years monthly)

    names = [f"Asset_{chr(65 + i)}" for i in range(n)]

    # Multi-factor return generation to ensure full rank and non-singular covariance
    drift = [0.005 + 0.005 * rng.random() for _ in range(n)]
    vol = [0.03 + 0.02 * rng.random() for _ in range(n)]
    beta1 = [0.6 + 0.8 * rng.random() for _ in range(n)]
    beta2 = [-0.3 + 0.6 * rng.random() for _ in range(n)]

    returns: list[list[float]] = []
    for _ in range(t):
        f1 = rng.gauss(0.0, 0.04)
        f2 = rng.gauss(0.0, 0.03)
        row: list[float] = []
        for i in range(n):
            idio = rng.gauss(0.0, vol[i])
            r = drift[i] + beta1[i] * f1 + beta2[i] * f2 + idio
            row.append(round(r, 6))
        returns.append(row)

    # Risk aversion parameter
    risk_aversion = round(2.0 + (seed % 5) * 0.5, 2)

    # Annualized target volatility (assuming monthly returns: sqrt(12) scale factor)
    target_vol = round(0.08 + (seed % 4) * 0.02, 3)

    # Maximum gross leverage
    max_leverage = round(1.5 + (seed % 3) * 0.5, 2)

    # Risk budgets: either equal or asymmetric
    raw_b = [1.0] * n if seed % 2 == 0 else [1.0 + (i * 0.5) for i in range(n)]
    tot_b = sum(raw_b)
    budgets = [round(b / tot_b, 6) for b in raw_b]
    budgets[0] += round(1.0 - sum(budgets), 6)

    # Expected returns for mean-variance
    mean = [round(sum(returns[row_idx][col_idx] for row_idx in range(t)) / t, 6) for col_idx in range(n)]

    return {
        "seed": seed,
        "n_assets": n,
        "n_obs": t,
        "names": names,
        "returns": returns,
        "mean": mean,
        "target_vol": target_vol,
        "risk_aversion": risk_aversion,
        "max_leverage": max_leverage,
        "budgets": budgets,
    }
