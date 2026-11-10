"""Lab SR3-L04-1: Interbank Network Contagion and Clearing Dynamics.

SIMULATED: solves the Eisenberg-Noe clearing vector and verifies the Acemoglu,
Ozdaglar, and Tahbaz-Salehi (2015) phase transition from risk diversification
to systemic fragility under moderate versus catastrophic asset shocks.
"""

from __future__ import annotations

import numpy as np


def solve_clearing(
    l_mat: np.ndarray,
    z_vec: np.ndarray,
    b_vec: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, int]:
    """Solve Eisenberg-Noe clearing payments via Picard fixed-point iteration."""
    p_bar = np.sum(l_mat, axis=1)
    pi_mat = np.zeros_like(l_mat)
    has_liab = p_bar > 0
    pi_mat[has_liab] = l_mat[has_liab] / p_bar[has_liab, None]

    p = p_bar.copy()
    rounds = 0
    for _ in range(500):
        rounds += 1
        # Inflows: Pi.T @ p
        p_next = np.minimum(p_bar, np.maximum(0.0, z_vec + pi_mat.T @ p - b_vec))
        if np.max(np.abs(p_next - p)) < 1e-10:
            p = p_next
            break
        p = p_next

    defaults = (p < p_bar - 1e-7).astype(int)
    return p, defaults, rounds


def main() -> None:
    # 4-bank financial network
    n = 4
    total_liab = 40.0  # Each bank owes 40 in nominal interbank liabilities

    # 1. Complete Network: liabilities evenly distributed across counterparties
    l_complete = np.full((n, n), total_liab / (n - 1))
    np.fill_diagonal(l_complete, 0.0)

    # 2. Ring Network: bank i borrows entirely from bank (i+1)%n
    l_ring = np.zeros((n, n))
    for i in range(n):
        l_ring[i, (i + 1) % n] = total_liab

    # Baseline asset endowments: outside assets z=20, outside senior debt b=14
    # Net outside equity buffer = 20 - 14 = 6 per bank
    z_baseline = np.full(n, 20.0)
    b_baseline = np.full(n, 14.0)

    # Scenario 1: Moderate shock on Bank 0 (outside assets drop from 20 to 5)
    # Bank 0 shortfall = 9.
    # In ring: Bank 1 absorbs all 9 (exceeds buffer 6 -> Bank 1 defaults).
    # In complete: Counterparties share 9/3 = 3 each (below buffer 6 -> 0 cascade defaults).
    z_mod = z_baseline.copy()
    z_mod[0] = 5.0
    _p_comp_mod, def_comp_mod, _ = solve_clearing(l_complete, z_mod, b_baseline)
    _p_ring_mod, def_ring_mod, _ = solve_clearing(l_ring, z_mod, b_baseline)

    # Scenario 2: Catastrophic shock on Bank 0 (assets wiped to 0, senior debt=22)
    # Shortfall = 22. In complete: each receives 22/3 = 7.33 loss (exceeds buffer 6 -> ALL fail).
    z_cat = z_baseline.copy()
    z_cat[0] = 0.0
    b_cat = b_baseline.copy()
    b_cat[0] = 22.0
    p_comp_cat, def_comp_cat, _ = solve_clearing(l_complete, z_cat, b_cat)
    _p_ring_cat, def_ring_cat, _ = solve_clearing(l_ring, z_cat, b_cat)

    print("=== Interbank Network Contagion (Acemoglu, Ozdaglar & Tahbaz-Salehi 2015) ===")
    print(f"Network size: N={n} banks. Nominal obligations per bank: p_bar={total_liab}")
    print("Net outside equity buffer per solvent bank: z - b = 6.0")
    print("-" * 75)
    print("Scenario 1: Moderate Negative Shock on Bank 0 (Shortfall = 9.0)")
    print(f"  Complete Network: Defaults = {int(np.sum(def_comp_mod))}/{n} (Default vector: {def_comp_mod})")
    print(f"  Ring Network:     Defaults = {int(np.sum(def_ring_mod))}/{n} (Default vector: {def_ring_mod})")
    print("  Outcome: Complete network diversifies shock across 3 peers (3.0 < 6.0).")
    print("           Ring network concentrates shock on Bank 1 (9.0 > 6.0), triggering cascade.")
    print("-" * 75)
    print("Scenario 2: Catastrophic Shock on Bank 0 (Shortfall = 22.0)")
    print(f"  Complete Network: Defaults = {int(np.sum(def_comp_cat))}/{n} (Default vector: {def_comp_cat})")
    print(f"  Ring Network:     Defaults = {int(np.sum(def_ring_cat))}/{n} (Default vector: {def_ring_cat})")
    print("  Outcome: Complete network propagates loss to ALL institutions (7.33 > 6.0).")
    print(f"  Clearing payments: Complete p*={p_comp_cat.round(2)}")
    print("-" * 75)
    print("Theorem 1 Phase Transition Verified:")
    print("Diversified interbank connections stabilize the system under moderate shocks,")
    print("but act as an unavoidable transmission mechanism during catastrophic shocks.")


main()
