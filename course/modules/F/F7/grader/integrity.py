"""Data integrity and structural invariant validation for F7 Due-Diligence Engine.

Ensures inputs and outputs adhere to econometric dimensions, lack NaNs/Infs,
and preserve mathematical invariants before and after manager evaluation.
"""

from __future__ import annotations

import numpy as np


def validate_due_diligence_instance(instance: dict[str, object]) -> bool:
    """Validate structure, types, shapes, and conditions of an instance."""
    required_keys = {
        "seed",
        "n_months",
        "factor_names",
        "factors",
        "mkt_excess",
        "manager_names",
        "manager_returns",
    }
    if not required_keys.issubset(instance.keys()):
        missing = required_keys - instance.keys()
        raise ValueError(f"Instance is missing required keys: {missing}")

    factors = np.asarray(instance["factors"], dtype=np.float64)
    mkt = np.asarray(instance["mkt_excess"], dtype=np.float64)
    returns = np.asarray(instance["manager_returns"], dtype=np.float64)

    if factors.ndim != 2 or factors.shape[1] < 1:
        raise ValueError("factors must be 2D array of shape (T, K)")
    if mkt.ndim != 1 or len(mkt) != factors.shape[0]:
        raise ValueError("mkt_excess must be 1D array matching factors length T")
    if returns.ndim != 2 or returns.shape[0] != factors.shape[0]:
        raise ValueError("manager_returns must be 2D array of shape (T, N_managers)")

    if not np.all(np.isfinite(factors)):
        raise ValueError("factors contains non-finite values (NaN or Inf)")
    if not np.all(np.isfinite(mkt)):
        raise ValueError("mkt_excess contains non-finite values (NaN or Inf)")
    if not np.all(np.isfinite(returns)):
        raise ValueError("manager_returns contains non-finite values (NaN or Inf)")

    return True


def validate_evaluation_output(output: list[dict[str, object]], n_expected: int) -> bool:
    """Validate output rankings, required fields, and order."""
    if len(output) != n_expected:
        raise ValueError(f"Expected {n_expected} evaluations, got {len(output)}")

    ranks = [int(str(x["rank"])) for x in output]
    if sorted(ranks) != list(range(1, n_expected + 1)):
        raise ValueError(f"Ranks must be a unique permutation of 1 to {n_expected}, got {ranks}")

    required_fields = {
        "name",
        "alpha_ann",
        "t_alpha",
        "sr_naive",
        "sr_adj",
        "xi",
        "vol_unsmoothed",
        "gamma",
        "t_gamma",
        "dd_score",
        "rank",
    }

    for ev in output:
        if not required_fields.issubset(ev.keys()):
            missing = required_fields - ev.keys()
            raise ValueError(f"Evaluation entry missing fields: {missing}")

    return True
