"""Lab 2: Equal Risk Contribution (ERC) numerical solver via log-barrier Newton method.

Demonstrates the Maillard-Roncalli-Teiletche (2010) log-barrier formulation:
min_y  0.5 * y.T @ Sigma @ y - sum_i (1/n) * ln(y_i)
with normalized weights w = y / sum(y), achieving exact equal risk contributions.
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
    n = 3
    b = np.full(n, 1.0 / n, dtype=np.float64)

    # Initial guess: inverse volatility
    diag_std = np.sqrt(np.diag(cov))
    inv_vol_w = (1.0 / diag_std) / np.sum(1.0 / diag_std)

    y = 1.0 / diag_std
    iterations = 0

    for i in range(1, 100):
        grad = cov @ y - b / y
        if float(np.max(np.abs(grad))) < 1e-10:
            iterations = i
            break
        hessian = cov + np.diag(b / (y**2))
        delta_y = np.linalg.solve(hessian, -grad)

        step = 1.0
        while np.any(y + step * delta_y <= 0):
            step *= 0.5
        y = y + step * delta_y

    w_erc = y / np.sum(y)
    port_vol = float(np.sqrt(w_erc @ cov @ w_erc))
    mrc = (cov @ w_erc) / port_vol
    trc = w_erc * mrc
    prc = trc / port_vol

    print(f"Newton Iterations to Convergence: {iterations}")
    print(f"Inverse-Vol Weights: {[round(float(x), 4) for x in inv_vol_w]}")
    print(f"ERC Weights: {[round(float(x), 4) for x in w_erc]}")
    print(f"ERC Portfolio Vol: {port_vol:.6f}")
    print(f"ERC Component TRC: {[round(float(x), 6) for x in trc]}")
    print(f"ERC Percent PRC: {[round(float(x), 6) for x in prc]}")
    print(f"Max PRC deviation from 1/N: {float(np.max(np.abs(prc - 1.0 / n))):.2e}")


main()
