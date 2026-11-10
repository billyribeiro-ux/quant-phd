"""Lab CAP3-L01-1: Proof Invariant & Matrix Conditioning Diagnostic under Exam Conditions.

Evaluates numerical stability of covariance inversions, positive-definiteness bounds,
and verifies no-arbitrage proof invariants under timed doctoral prelim conditions.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # 1. Construct a calibrated asset covariance matrix (4 test assets)
    np.random.seed(42)
    volatilities = np.array([0.15, 0.20, 0.18, 0.25])
    correlation = np.array(
        [
            [1.00, 0.45, 0.30, 0.55],
            [0.45, 1.00, 0.40, 0.60],
            [0.30, 0.40, 1.00, 0.35],
            [0.55, 0.60, 0.35, 1.00],
        ]
    )
    cov_matrix = np.outer(volatilities, volatilities) * correlation

    # 2. Condition number and spectral decomposition
    eigenvalues = np.linalg.eigvalsh(cov_matrix)
    cond_number = float(np.max(eigenvalues) / np.min(eigenvalues))
    is_positive_definite = bool(np.all(eigenvalues > 0.0))

    # 3. Mean excess returns
    mu_excess = np.array([0.06, 0.08, 0.05, 0.09])

    # 4. Tangency portfolio weights and maximum Sharpe ratio invariant
    inv_cov = np.linalg.inv(cov_matrix)
    tangency_weights = inv_cov @ mu_excess
    tangency_weights /= np.sum(tangency_weights)
    tangency_return = float(tangency_weights @ mu_excess)
    tangency_variance = float(tangency_weights @ cov_matrix @ tangency_weights)
    tangency_vol = float(np.sqrt(tangency_variance))
    sharpe_ratio = float(tangency_return / tangency_vol)

    # 5. Quadratic form verification: SR = sqrt(mu^T Sigma^{-1} mu)
    analytical_sr = float(np.sqrt(mu_excess @ inv_cov @ mu_excess))

    print(f"Condition Number: {cond_number:.2f}")
    print(f"Positive Definite: {is_positive_definite}")
    print(f"Tangency Weights: {[round(float(w), 4) for w in tangency_weights]}")
    print(f"Tangency Mean Return: {tangency_return:.4f}")
    print(f"Tangency Volatility: {tangency_vol:.4f}")
    print(f"Tangency Sharpe Ratio: {sharpe_ratio:.4f}")
    print(f"Quadratic Form SR: {analytical_sr:.4f}")
    print(f"Invariant Match Error: {abs(sharpe_ratio - analytical_sr):.2e}")


main()
