"""CS1 lab L07: NumPy arrays, broadcasting, and vectorization vs. Python loops.

Demonstrates contiguous memory buffers, multidimensional broadcasting, and verifies
that vectorized array arithmetic matches iterative loops to float tolerance.
SIMULATED seeded asset returns and weights.
"""

from __future__ import annotations

import numpy as np


def compute_portfolio_returns_loop(returns: list[list[float]], weights: list[float]) -> list[float]:
    """Compute portfolio returns across time periods using explicit nested loops."""
    periods = len(returns)
    assets = len(weights)
    out: list[float] = [0.0] * periods
    for t in range(periods):
        period_sum = 0.0
        for i in range(assets):
            period_sum += returns[t][i] * weights[i]
        out[t] = period_sum
    return out


def main() -> None:
    # 1. Seeded SIMULATED data
    rng = np.random.default_rng(42)
    periods = 5
    assets = 3
    # Returns matrix: 5 periods x 3 assets
    sim_returns = rng.normal(loc=0.001, scale=0.02, size=(periods, assets))
    weights = np.array([0.5, 0.3, 0.2])

    # 2. Vectorized calculation via broadcasting and reduction
    vectorized_port_returns = np.sum(sim_returns * weights, axis=1)

    # 3. Explicit Python loop calculation
    returns_list = sim_returns.tolist()
    weights_list = weights.tolist()
    loop_port_returns = compute_portfolio_returns_loop(returns_list, weights_list)

    # 4. Compare results
    max_abs_diff = float(np.max(np.abs(vectorized_port_returns - np.array(loop_port_returns))))
    equal_to_tol = max_abs_diff < 1e-12

    print(f"array shape: {sim_returns.shape}")
    print(f"array dtype: {sim_returns.dtype}")
    print(f"weights shape: {weights.shape}")
    print(f"vectorized return period 0: {vectorized_port_returns[0]:.6f}")
    print(f"loop return period 0: {loop_port_returns[0]:.6f}")
    print(f"maximum absolute difference: {max_abs_diff:.2e}")
    print(f"vectorized and loop results equal to 1e-12: {equal_to_tol}")
    print(f"loop iterations: {periods * assets}, vectorized calls: 1")


main()
