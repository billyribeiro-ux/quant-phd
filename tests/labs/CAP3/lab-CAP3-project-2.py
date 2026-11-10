"""Lab CAP3-project-2: Worked Example: Field Prelim I Complete Analytical Verification.

Verifies the worked example solution of Hansen-Jagannathan SDF bounds,
tangency portfolio weights, and continuous-time Merton portfolio optimization.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # Worked example parameters from project.html
    rf = 0.02
    mu = np.array([0.07, 0.09, 0.05])
    cov = np.array(
        [
            [0.040, 0.012, 0.008],
            [0.012, 0.060, 0.015],
            [0.008, 0.015, 0.030],
        ]
    )
    gamma = 5.0

    # Step 1: Invert covariance and compute tangency portfolio
    cov_inv = np.linalg.inv(cov)
    tangency_raw = cov_inv @ mu
    tangency_weights = tangency_raw / np.sum(tangency_raw)
    sr_tangency = float(np.sqrt(mu @ cov_inv @ mu))

    # Step 2: Hansen-Jagannathan bound for E[m] = 1 / (1 + rf)
    mean_sdf = 1.0 / (1.0 + rf)
    hj_lower_bound = mean_sdf * sr_tangency

    # Step 3: Merton continuous-time portfolio share
    sigma_first = float(np.sqrt(cov[0, 0]))
    merton_fraction = mu[0] / (gamma * (sigma_first**2))

    print(f"Worked Example Tangency Weights: {[round(float(w), 4) for w in tangency_weights]}")
    print(f"Tangency Portfolio Sharpe Ratio: {sr_tangency:.4f}")
    print(f"Hansen-Jagannathan Bound on Std(m): {hj_lower_bound:.4f}")
    print(f"Merton Optimal Stock Share: {merton_fraction:.4f}")


main()
