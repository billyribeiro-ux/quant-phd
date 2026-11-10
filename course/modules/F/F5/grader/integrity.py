"""Input and output integrity validation for F5: Replication-Crisis Adjudication Engine.

Provides input validation, matrix condition checks, and structural invariants
guaranteeing data integrity before and after adjudication.
"""

from __future__ import annotations

import numpy as np


def validate_factor_panel(returns: np.ndarray, name: str = "returns") -> np.ndarray:
    """Validate a factor return panel (N_candidates x T_months)."""
    arr = np.asarray(returns, dtype=np.float64)
    if arr.ndim != 2:
        raise ValueError(f"{name} must be 2D array of shape (N, T), got {arr.ndim}D")
    if arr.shape[0] < 1 or arr.shape[1] < 12:
        raise ValueError(f"{name} requires at least 1 candidate and 12 periods")
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"{name} contains non-finite values (NaN/Inf)")
    return arr


def validate_control_factors(controls: np.ndarray) -> np.ndarray:
    """Validate control factor returns matrix (T_months x K_controls)."""
    arr = np.asarray(controls, dtype=np.float64)
    if arr.ndim != 2:
        raise ValueError(f"controls must be 2D array of shape (T, K), got {arr.ndim}D")
    if arr.shape[0] < 12 or arr.shape[1] < 1:
        raise ValueError("controls requires at least 12 periods and 1 factor")
    if not np.all(np.isfinite(arr)):
        raise ValueError("controls contains non-finite values (NaN/Inf)")
    return arr


def validate_adjudication_outputs(adjudication: dict[str, object]) -> bool:
    """Validate structural invariants of adjudication output dictionary."""
    required_keys = {
        "candidate_names",
        "replication",
        "multiple_testing",
        "bayes_shrinkage",
        "ds_retained",
        "ds_t_stats",
        "classifications",
        "classification_counts",
    }
    if not required_keys.issubset(adjudication.keys()):
        missing = required_keys - adjudication.keys()
        raise ValueError(f"Missing required adjudication output keys: {missing}")

    raw_classes = adjudication["classifications"]
    classifications = [str(x) for x in raw_classes] if isinstance(raw_classes, (list, tuple, np.ndarray)) else []
    valid_classes = {"ROBUST", "MICROCAP_ONLY", "SPANNED", "DATA_SNOOPING"}
    for c in classifications:
        if c not in valid_classes:
            raise ValueError(f"Unknown classification category '{c}'")

    return True
