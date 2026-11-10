"""Lab QR3-project-1: Rung 2 Completion Problem Reference Solution.

Implements the three core algorithmic building blocks of Atlas A17:
1. Cyclical coordinate descent soft-thresholding operator.
2. Purged cross-validation boundary index calculation.
3. TreeSHAP local additivity axiom verification.
"""

from __future__ import annotations

import math

import numpy as np


def soft_threshold(z: float, gamma: float) -> float:
    """Computes soft-thresholding operator S(z, gamma) = sign(z) * max(|z| - gamma, 0)."""
    if z > gamma:
        return z - gamma
    elif z < -gamma:
        return z + gamma
    return 0.0


def compute_purge_boundaries(
    test_start: int,
    test_end: int,
    label_lookahead: int,
    embargo_pct: float,
    n_samples: int,
) -> tuple[int, int]:
    """Computes start of left-purge window and end of post-test embargo window."""
    purge_start = max(0, test_start - label_lookahead + 1)
    h_embargo = math.ceil(embargo_pct * n_samples)
    embargo_end = min(n_samples - 1, test_end + h_embargo)
    return purge_start, embargo_end


def verify_shap_additivity(base_val: float, phi: np.ndarray, pred_val: float, tol: float = 1e-7) -> bool:
    """Verifies that TreeSHAP attributions satisfy the local additivity axiom."""
    total = base_val + float(np.sum(phi))
    return math.isclose(total, pred_val, abs_tol=tol)


def main() -> None:
    # 1. Soft-thresholding checks
    z_vals = [2.5, -3.0, 0.4, -0.2]
    gamma = 0.5
    st_results = [soft_threshold(z, gamma) for z in z_vals]
    print(f"Soft-thresholding with gamma={gamma}:")
    for z, st in zip(z_vals, st_results, strict=True):
        print(f"  S({z:+.2f}, {gamma}) = {st:+.2f}")

    # 2. Purge boundary checks
    n_samples = 250
    t_start = 50
    t_end = 99
    lookahead = 5
    embargo_pct = 0.02
    p_start, e_end = compute_purge_boundaries(t_start, t_end, lookahead, embargo_pct, n_samples)
    print(f"\nPurged CV Boundaries for Test Fold [{t_start}, {t_end}]:")
    print(f"  Purge Window Starts at Index: {p_start}")
    print(f"  Embargo Window Ends at Index: {e_end}")
    print(f"  Purged Samples on Left Boundary: {t_start - p_start}")
    print(f"  Embargoed Samples on Right Boundary: {e_end - t_end}")

    # 3. TreeSHAP additivity verification
    phi_0 = 1.25
    phi_vec = np.array([0.45, -0.80, 0.10, 0.00])
    target_pred = 1.00
    is_valid = verify_shap_additivity(phi_0, phi_vec, target_pred)
    print("\nTreeSHAP Additivity Check:")
    print(f"  phi_0: {phi_0:.2f} | sum(phi): {np.sum(phi_vec):+.2f} | f(x): {target_pred:.2f}")
    print(f"  Additivity Axiom Satisfied: {is_valid}")
    print("Completion lab twin executed successfully.")


main()
