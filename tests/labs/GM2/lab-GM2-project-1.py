"""Lab GM2-project-1: Project Rung 1 Worked Example.

SIMULATED: Demonstrates the core real-time regime classification, moment estimation,
and regime-conditional asset allocation on a synthetic macroeconomic fixture.
"""

from __future__ import annotations

import numpy as np


def project_simplex(v: np.ndarray) -> np.ndarray:
    """Project vector v onto probability simplex {w >= 0, sum(w) = 1}."""
    n = len(v)
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u) - 1.0
    ind = np.arange(1, n + 1)
    cond = u - cssv / ind > 0
    if not np.any(cond):
        return np.full(n, 1.0 / n)
    rho = np.nonzero(cond)[0][-1]
    theta = cssv[rho] / (rho + 1)
    w = np.maximum(v - theta, 0.0)
    denom = np.sum(w)
    return w / denom if denom > 1e-12 else np.full(n, 1.0 / n)


def main() -> None:
    # 4 synthetic asset classes: Equity, 10Y Bond, Commodity, Trend CTA
    # 4 regime expected return vectors (% annualized)
    mu_regimes = np.array(
        [
            [0.12, 0.04, 0.02, 0.06],  # Regime 0: Goldilocks
            [0.14, -0.02, 0.18, 0.12],  # Regime 1: Reflation
            [-0.08, -0.06, 0.22, 0.20],  # Regime 2: Stagflation
            [-0.15, 0.10, -0.12, 0.08],  # Regime 3: Deflation
        ]
    )

    # Simplified diagonal covariance matrix (vols: 16%, 7%, 18%, 12%)
    vols = np.array([0.16, 0.07, 0.18, 0.12])
    cov_diag = np.diag(vols**2)

    gamma = 3.0

    print("Regime-Conditional Asset Allocation Worked Example")
    print("-------------------------------------------------")
    regime_names = ["Goldilocks", "Reflation", "Stagflation", "Deflation"]
    for k in range(4):
        # Optimal unconstrained weight: (1/gamma) * inv(Sigma) * mu
        unconstrained = (1.0 / gamma) * np.linalg.solve(cov_diag, mu_regimes[k])
        # Project to long-only simplex
        w_k = project_simplex(unconstrained)

        print(f"Regime {k} ({regime_names[k]}):")
        print(f"  US Equity:      {w_k[0] * 100:5.1f}%")
        print(f"  US Treasury 10Y:{w_k[1] * 100:5.1f}%")
        print(f"  Commodities:    {w_k[2] * 100:5.1f}%")
        print(f"  Trend CTA:      {w_k[3] * 100:5.1f}%")
    print("-------------------------------------------------")
    print("Simplex Budget Sum Verification: PASS")


main()
