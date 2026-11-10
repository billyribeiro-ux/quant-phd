"""Lab 1: Euler risk decomposition and marginal risk contributions.

Demonstrates Euler's homogeneous function theorem on portfolio volatility:
sigma_p = sum(w_i * MRC_i) = sum(TRC_i), and sum(PRC_i) = 1.0.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # 3-asset covariance matrix: Equities (18%), Bonds (6%), Commodities (15%)
    cov = np.array(
        [
            [0.0324, 0.0020, 0.0050],
            [0.0020, 0.0036, -0.0010],
            [0.0050, -0.0010, 0.0225],
        ],
        dtype=np.float64,
    )

    # Traditional 60/40 balanced asset allocation with commodities (50% eq, 40% fi, 10% com)
    weights = np.array([0.50, 0.40, 0.10], dtype=np.float64)

    port_var = float(weights @ cov @ weights)
    port_vol = float(np.sqrt(port_var))

    # Marginal risk contribution: d(sigma_p)/dw_i = (Sigma @ w)_i / sigma_p
    mrc = (cov @ weights) / port_vol

    # Total (component) risk contribution: TRC_i = w_i * MRC_i
    trc = weights * mrc

    # Percent risk contribution: PRC_i = TRC_i / sigma_p
    prc = trc / port_vol

    print(f"Portfolio Volatility: {port_vol:.6f}")
    print(f"Weights: {[round(float(x), 4) for x in weights]}")
    print(f"MRC: {[round(float(x), 6) for x in mrc]}")
    print(f"TRC: {[round(float(x), 6) for x in trc]}")
    print(f"PRC: {[round(float(x), 6) for x in prc]}")
    print(f"Euler sum(TRC): {float(np.sum(trc)):.6f}")
    print(f"Sum PRC: {float(np.sum(prc)):.6f}")
    print(f"Equity Risk Share: {prc[0] * 100:.2f}%")


main()
