"""Rung 1 worked example: Atlas A11 portfolio construction pipeline.

Illustrative 4-asset return window over 6 periods:
1. Sample covariance matrix calculation.
2. Ledoit-Wolf linear shrinkage toward scaled identity.
3. Equal Risk Contribution (ERC) portfolio via Newton log-barrier solver.
4. Component and percent risk contributions verifying Euler's theorem.
5. Volatility-targeted weights with gross leverage capping.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # 4 assets over 6 observation periods (T = 6, N = 4)
    returns = np.array(
        [
            [0.02, 0.01, 0.03, -0.01],
            [0.04, 0.02, -0.01, 0.03],
            [-0.01, 0.03, 0.02, 0.01],
            [0.03, -0.01, 0.04, -0.02],
            [0.01, 0.04, 0.01, 0.02],
            [0.03, 0.03, 0.03, 0.01],
        ],
        dtype=np.float64,
    )
    t, n = returns.shape

    # Step 1: Sample covariance
    mean_ret = np.mean(returns, axis=0)
    centered = returns - mean_ret
    sample_cov = (centered.T @ centered) / (t - 1)

    # Step 2: Ledoit-Wolf linear shrinkage toward scaled identity
    mu_var = float(np.trace(sample_cov) / n)
    target_mat = mu_var * np.eye(n, dtype=np.float64)
    d2 = float(np.sum((sample_cov - target_mat) ** 2))
    q = np.zeros((n, n), dtype=np.float64)
    for k in range(t):
        dev = np.outer(centered[k], centered[k]) - sample_cov
        q += dev**2
    b2 = float(np.sum(q) / (t**2))
    delta = max(0.0, min(1.0, b2 / d2))
    shrunk_cov = (1.0 - delta) * sample_cov + delta * target_mat
    shrunk_cov = 0.5 * (shrunk_cov + shrunk_cov.T)

    # Step 3: Equal Risk Contribution weights via Newton solver
    b = np.full(n, 1.0 / n, dtype=np.float64)
    y = 1.0 / np.sqrt(np.diag(shrunk_cov))
    for _ in range(50):
        grad = shrunk_cov @ y - b / y
        if float(np.max(np.abs(grad))) < 1e-10:
            break
        hess = shrunk_cov + np.diag(b / (y**2))
        dy = np.linalg.solve(hess, -grad)
        step = 1.0
        while np.any(y + step * dy <= 0):
            step *= 0.5
        y = y + step * dy

    w_erc = y / np.sum(y)

    # Step 4: Component and percent risk contributions
    port_vol = float(np.sqrt(w_erc @ shrunk_cov @ w_erc))
    mrc = (shrunk_cov @ w_erc) / port_vol
    trc = w_erc * mrc
    prc = trc / port_vol

    # Step 5: Volatility targeting at 10% target vol with 1.5x gross leverage cap
    target_vol = 0.10
    scale = target_vol / port_vol
    w_vt = scale * w_erc
    gross_lev = float(np.sum(np.abs(w_vt)))
    cap = 1.50
    if gross_lev > cap:
        w_vt = w_vt * (cap / gross_lev)

    print(f"Step 1 Sample Cov Diagonal: {[round(float(x), 6) for x in np.diag(sample_cov)]}")
    print(f"Step 2 Shrinkage Delta: {delta:.4f}")
    print(f"Step 2 Shrunk Cov Diagonal: {[round(float(x), 6) for x in np.diag(shrunk_cov)]}")
    print(f"Step 3 ERC Weights: {[round(float(x), 4) for x in w_erc]}")
    print(f"Step 4 Portfolio Volatility: {port_vol:.6f}")
    print(f"Step 4 Percent Risk Contributions: {[round(float(x), 4) for x in prc]}")
    print(f"Step 5 Uncapped Leverage: {gross_lev:.4f}x")
    print(f"Step 5 Vol-Target Weights (Capped at {cap:.2f}x): {[round(float(x), 4) for x in w_vt]}")


main()
