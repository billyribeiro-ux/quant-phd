"""Lab CAP3-L02-1: Field Prelim I, Problem A: Hansen-Jagannathan Volatility Bound.

Derives and computes the Hansen-Jagannathan (1991) SDF volatility bound
across candidate expected discount factors E[m] using sample asset returns.
"""

from __future__ import annotations

import numpy as np


def compute_hj_bound(
    mean_gross_returns: np.ndarray,
    cov_gross_returns: np.ndarray,
    mean_m: float,
) -> float:
    """Compute the Hansen-Jagannathan lower bound on SDF volatility for a given E[m]."""
    n_assets = len(mean_gross_returns)
    ones = np.ones(n_assets)
    # Excess pricing error vector: e_m = E[m R] - 1 = mean_m * R_bar - 1
    pricing_errors = mean_m * mean_gross_returns - ones
    cov_inv = np.linalg.inv(cov_gross_returns)
    quad_form = float(pricing_errors @ cov_inv @ pricing_errors)
    return float(np.sqrt(max(0.0, quad_form)))


def main() -> None:
    # Calibrated gross return parameters (equity index and 10-year Treasury)
    mean_gross = np.array([1.08, 1.04])
    cov_gross = np.array([[0.0324, 0.0036], [0.0036, 0.0064]])

    # Candidate values for E[m] corresponding to annualized risk-free rates from 1% to 5%
    candidate_rf = [0.01, 0.02, 0.03, 0.04, 0.05]
    print("--- Hansen-Jagannathan Volatility Frontier ---")
    for rf in candidate_rf:
        mean_m = 1.0 / (1.0 + rf)
        sigma_m_min = compute_hj_bound(mean_gross, cov_gross, mean_m)
        max_sharpe = sigma_m_min / mean_m
        print(
            f"Rf = {rf * 100:.1f}% | E[m] = {mean_m:.4f} | "
            f"Min Std(m) = {sigma_m_min:.4f} | Bound Ratio = {max_sharpe:.4f}"
        )


main()
