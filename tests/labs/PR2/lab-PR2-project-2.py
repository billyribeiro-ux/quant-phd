"""Rung 2 completed solution: Atlas A11 portfolio construction with completed steps.

Completes the portfolio construction pipeline:
1. Percent risk contribution calculation from component risk contributions.
2. Volatility targeting weight scaling.
3. Gross leverage constraint enforcement.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
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

    mean_ret = np.mean(returns, axis=0)
    centered = returns - mean_ret
    sample_cov = (centered.T @ centered) / (t - 1)

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

    port_vol = float(np.sqrt(w_erc @ shrunk_cov @ w_erc))
    mrc = (shrunk_cov @ w_erc) / port_vol
    trc = w_erc * mrc
    # Completed line: percent risk contribution
    prc = trc / port_vol

    target_vol = 0.10
    # Completed line: target volatility scale factor
    scale = target_vol / port_vol
    w_vt = scale * w_erc
    gross_lev = float(np.sum(np.abs(w_vt)))
    cap = 1.50
    if gross_lev > cap:
        # Completed line: leverage cap scaling
        w_vt = w_vt * (cap / gross_lev)

    print(f"Completed PRC: {[round(float(x), 4) for x in prc]}")
    print(f"Completed Target Vol Scale: {scale:.4f}")
    print(f"Completed Vol-Target Weights: {[round(float(x), 4) for x in w_vt]}")
    print(f"Final Realized Gross Leverage: {float(np.sum(np.abs(w_vt))):.4f}")


main()
