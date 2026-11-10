"""Lab PR5-project-2: Project Rung 2 Completion Problem Twin.

SIMULATED: Solution twin for drawdown cushion computation and multi-pod capital allocation.
"""

from __future__ import annotations

import numpy as np


def compute_cushion_and_weights(
    current_drawdowns: np.ndarray,
    hard_stops: np.ndarray,
    sigmas: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate pod cushions, risk parity weights, and cushion-adjusted weights."""
    # Step 1: Compute distance-to-stop cushions C_i = max(0, hard_stop_i - D_i)
    cushions = np.maximum(0.0, hard_stops - current_drawdowns)

    # Step 2: Compute inverse-volatility risk parity weights
    inv_vols = 1.0 / sigmas
    w_risk_parity = inv_vols / np.sum(inv_vols)

    # Step 3: Compute drawdown-budgeted cushion weights w_i proportional to C_i / sigma_i
    raw_scores = cushions / sigmas
    w_cushion = raw_scores / np.sum(raw_scores)

    return cushions, w_risk_parity, w_cushion


def main() -> None:
    # 4 active pods with current drawdowns, stops, and volatilities
    current_drawdowns = np.array([0.02, 0.05, 0.07, 0.01])
    hard_stops = np.array([0.08, 0.08, 0.08, 0.08])
    sigmas = np.array([0.15, 0.20, 0.12, 0.18])

    cushions, w_rp, w_cush = compute_cushion_and_weights(
        current_drawdowns=current_drawdowns,
        hard_stops=hard_stops,
        sigmas=sigmas,
    )

    print("Project Rung 2 · Completion Lab: Multi-Pod Drawdown Cushion & Weights")
    print("=" * 68)
    print(f"{'Pod':<6} {'DD':<8} {'Stop':<8} {'Cushion':<10} {'Risk Parity':<14} {'Cushion Weight':<14}")
    print("-" * 68)
    for i in range(len(current_drawdowns)):
        print(
            f"Pod {i + 1:<2} {current_drawdowns[i] * 100:<7.1f}% {hard_stops[i] * 100:<7.1f}% "
            f"{cushions[i] * 100:<9.1f}% {w_rp[i] * 100:<13.2f}% {w_cush[i] * 100:<13.2f}%"
        )


main()
