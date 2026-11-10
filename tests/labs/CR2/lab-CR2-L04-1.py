"""Lab CR2-L04-1: One-factor Gaussian copula loss distribution and Large Homogeneous Portfolio (LHP) VaR.

Demonstrates Li (2000) latent factor conditioning, verifies unconditional expected loss invariance,
and quantifies tail risk expansion under increasing asset correlation.
"""

from __future__ import annotations

import math

import numpy as np
from scipy import stats


def main() -> None:
    # Portfolio parameters
    num_names = 125
    default_prob = 0.05  # 5.0% 5Y cumulative default probability
    recovery = 0.40  # 40% recovery
    correlations = [0.01, 0.10, 0.20, 0.35, 0.50]

    # Gauss-Legendre quadrature over systematic market factor M
    num_points = 80
    nodes, weights = np.polynomial.legendre.leggauss(num_points)
    m_nodes = nodes * 5.0
    w_nodes = weights * 5.0

    inv_p = float(stats.norm.ppf(default_prob))
    inv_99 = float(stats.norm.ppf(0.99))
    inv_999 = float(stats.norm.ppf(0.999))

    print(f"One-Factor Gaussian Copula Loss Distribution (N={num_names}, p=5.0%, R=40%):")
    print("  Correlation rho | Expected Loss | Loss Vol (std) |  99.0% LHP VaR | 99.9% LHP VaR")
    print("------------------+---------------+----------------+----------------+---------------")

    for rho in correlations:
        sigma_idio = math.sqrt(max(1e-10, 1.0 - rho))
        cond_p = stats.norm.cdf((inv_p - math.sqrt(rho) * m_nodes) / sigma_idio)
        loss_m = (1.0 - recovery) * cond_p
        phi_m = stats.norm.pdf(m_nodes)

        exp_loss = float(np.sum(loss_m * phi_m * w_nodes))
        loss_sq = float(np.sum((loss_m**2) * phi_m * w_nodes))
        loss_std = math.sqrt(max(0.0, loss_sq - exp_loss**2))

        # Analytical Vasicek / LHP quantiles
        p_99 = float(stats.norm.cdf((inv_p + math.sqrt(rho) * inv_99) / sigma_idio))
        var_99 = (1.0 - recovery) * p_99

        p_999 = float(stats.norm.cdf((inv_p + math.sqrt(rho) * inv_999) / sigma_idio))
        var_999 = (1.0 - recovery) * p_999

        print(
            f"       {rho:4.2f}       |     {exp_loss * 100:5.2f}%     |     "
            f"{loss_std * 100:5.2f}%      |     {var_99 * 100:5.2f}%     |    {var_999 * 100:5.2f}%"
        )

        # Invariant: Expected loss is invariant to correlation rho
        assert abs(exp_loss - (1.0 - recovery) * default_prob) < 1e-4

    print("\nTower Property Verification:")
    print("  E[Loss] = (1 - R) * p = (1 - 0.40) * 0.05 = 3.00% across all correlation values.")
    print("  Correlation governs the dispersion and tail shape of portfolio losses, not the mean.")


main()
