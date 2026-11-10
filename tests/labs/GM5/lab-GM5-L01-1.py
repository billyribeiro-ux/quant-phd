"""Lab GM5-L01-1: Crisis Mechanism Mapping & Systemic Contagion Simulation.

Simulates network contagion and balance sheet cascade propagation across financial institutions
with interbank obligations, measuring default cascades and amplification multipliers.
"""

from __future__ import annotations

from typing import Any

import numpy as np


def simulate_network_contagion(
    equities: np.ndarray,
    interbank_matrix: np.ndarray,
    external_assets: np.ndarray,
    initial_shock: np.ndarray,
    fire_sale_discount: float = 0.20,
) -> dict[str, Any]:
    """Simulate systemic Eisenberg-Noe network contagion with fire-sale amplification.

    Parameters
    ----------
    equities : np.ndarray
        Initial equity capital per node in millions of dollars.
    interbank_matrix : np.ndarray
        Interbank liabilities matrix L where L[i, j] is debt owed by i to j.
    external_assets : np.ndarray
        Nominal value of external illiquid assets held per node.
    initial_shock : np.ndarray
        Exogenous asset devaluation shock per node in [0, 1].
    fire_sale_discount : float
        Proportional fire-sale discount applied when defaulted institutions liquidate assets.

    Returns
    -------
    dict[str, float | int | list[int]]
        Summary statistics including total defaults, cascade rounds, and total equity loss.
    """
    n_nodes = len(equities)
    current_equities = equities.copy()
    current_assets = external_assets.copy()
    defaulted = np.zeros(n_nodes, dtype=bool)

    # Apply initial external asset shock
    current_assets = current_assets * (1.0 - initial_shock)
    current_equities = current_equities - external_assets * initial_shock

    newly_defaulted = np.where((current_equities <= 0.0) & (~defaulted))[0]
    rounds = 0
    defaults_by_round: list[int] = []

    while len(newly_defaulted) > 0:
        rounds += 1
        defaulted[newly_defaulted] = True
        defaults_by_round.append(len(newly_defaulted))

        # Contagion via interbank exposures and asset fire sales
        for d in newly_defaulted:
            # Loss passed to creditors: pro-rata shortfall
            liabilities_d = np.sum(interbank_matrix[d, :])
            if liabilities_d > 0:
                shortfall = max(0.0, -current_equities[d])
                recovery_rate = max(0.0, 1.0 - shortfall / liabilities_d)
                loss_to_creditors = interbank_matrix[d, :] * (1.0 - recovery_rate)
                current_equities -= loss_to_creditors

            # Secondary fire-sale externality on external asset prices
            current_equities -= external_assets * fire_sale_discount * (1.0 / n_nodes)

        newly_defaulted = np.where((current_equities <= 0.0) & (~defaulted))[0]

    total_defaults = int(np.sum(defaulted))
    total_loss = float(np.sum(equities - np.maximum(0.0, current_equities)))
    amplification = total_loss / max(1e-6, float(np.sum(external_assets * initial_shock)))

    return {
        "total_defaults": total_defaults,
        "cascade_rounds": rounds,
        "total_equity_loss": total_loss,
        "amplification_multiplier": amplification,
        "defaults_by_round": defaults_by_round,
    }


def main() -> None:
    rng = np.random.default_rng(42)
    n_institutions = 10

    # Nominal balance sheets in millions USD
    equities = np.array([50.0 + 10.0 * i for i in range(n_institutions)], dtype=np.float64)
    external_assets = equities * 8.0  # 8x leverage

    # Core-periphery interbank liabilities matrix
    interbank = rng.uniform(5.0, 25.0, size=(n_institutions, n_institutions))
    np.fill_diagonal(interbank, 0.0)

    # Initial idiosyncratic shock hitting the most leveraged core node (Node 0)
    shock = np.zeros(n_institutions, dtype=np.float64)
    shock[0] = 0.22  # 22% asset writedown on node 0

    results = simulate_network_contagion(
        equities=equities,
        interbank_matrix=interbank,
        external_assets=external_assets,
        initial_shock=shock,
        fire_sale_discount=0.15,
    )

    print("Initial Shocked Nodes:", int(np.sum(shock > 0)))
    print("Total Insolvent Nodes:", results["total_defaults"])
    print("Contagion Cascade Rounds:", results["cascade_rounds"])
    print("Defaults by Round:", results["defaults_by_round"])
    print("Total System Equity Loss ($M):", round(float(results["total_equity_loss"]), 2))
    print("Contagion Amplification Multiplier:", round(float(results["amplification_multiplier"]), 4))


main()
