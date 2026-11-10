"""Lab SR3-project-2 (Rung 2 Completion Problem): Eisenberg-Noe Network Clearing.

SIMULATED: completion twin for the Eisenberg-Noe financial network clearing engine.
Implements the relative liability transition matrix, interbank inflow aggregation,
and the Picard fixed-point contraction operator.
"""

from __future__ import annotations

import numpy as np


def solve_eisenberg_noe(
    l_mat: np.ndarray,
    z_vec: np.ndarray,
    b_vec: np.ndarray,
    tol: float = 1e-10,
    max_iter: int = 500,
) -> tuple[np.ndarray, np.ndarray, int, float]:
    """Compute the clearing payment vector p* under Eisenberg-Noe (2001)."""
    p_bar = np.sum(l_mat, axis=1)

    # Relative liabilities matrix Pi: Pi[i, j] = L[i, j] / p_bar[i]
    pi_mat = np.zeros_like(l_mat)
    has_obligations = p_bar > 1e-12
    pi_mat[has_obligations] = l_mat[has_obligations] / p_bar[has_obligations, None]

    # Initialize at full nominal payments p = p_bar
    p = p_bar.copy()
    rounds = 0

    for _ in range(max_iter):
        rounds += 1
        # Interbank payment inflows to institution i: sum_j Pi[j, i] * p[j]
        inflows = pi_mat.T @ p

        # Eisenberg-Noe lattice operator: min(p_bar, max(0, z + inflows - b))
        p_next = np.minimum(p_bar, np.maximum(0.0, z_vec + inflows - b_vec))

        if np.max(np.abs(p_next - p)) < tol:
            p = p_next
            break
        p = p_next

    defaults = (p < p_bar - 1e-7).astype(int)
    total_shortfall = float(np.sum(p_bar - p))
    return p, defaults, rounds, total_shortfall


def main() -> None:
    # 5-node interbank network fixture
    l_mat = np.array(
        [
            [0.0, 25.0, 15.0, 10.0, 0.0],
            [10.0, 0.0, 20.0, 10.0, 10.0],
            [15.0, 15.0, 0.0, 20.0, 10.0],
            [5.0, 15.0, 15.0, 0.0, 15.0],
            [10.0, 10.0, 10.0, 20.0, 0.0],
        ]
    )
    p_bar = np.sum(l_mat, axis=1)

    # External assets z and senior liabilities b
    z_stressed = np.array([0.0, 20.0, 25.0, 18.0, 22.0])  # Node 0 asset collapse
    b_senior = np.array([15.0, 12.0, 14.0, 10.0, 11.0])

    p_star, defaults, rounds, shortfall = solve_eisenberg_noe(l_mat, z_stressed, b_senior)

    print("=== Eisenberg-Noe Network Clearing Solution (Completion) ===")
    print(f"Nodes in Network: {len(p_bar)}")
    print(f"Total Nominal Liabilities: ${np.sum(p_bar):.1f}B")
    print("-" * 65)
    print(f"Picard Contraction Iterations: {rounds}")
    print(f"Defaulting Institutions: {int(np.sum(defaults))}/{len(p_bar)} (Default vector: {defaults})")
    print(f"Total Systemic Shortfall: ${shortfall:.2f}B")
    print("-" * 65)
    for i in range(len(p_bar)):
        status = "DEFAULT" if defaults[i] else "SOLVENT"
        print(f"Node {i}: Promised ${p_bar[i]:<5.1f}B | Paid ${p_star[i]:<5.2f}B | Status: {status}")


main()
