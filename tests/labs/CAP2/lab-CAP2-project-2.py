"""Lab CAP2-project-2: Solution twin for completion problem on shrinkage and decay.

Implements the completed logic for Empirical Bayes precision weighting and
out-of-sample decay verification.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def run_completion_pipeline() -> None:
    rng = np.random.default_rng(42)

    # 1. Inputs: 6 anomaly return estimates with heterogeneous standard errors
    empirical_means = np.array([0.0092, 0.0068, 0.0055, 0.0041, 0.0083, 0.0031])
    standard_errors = np.array([0.0020, 0.0022, 0.0028, 0.0019, 0.0024, 0.0025])

    # Empirical Bayes cross-sectional variance tau^2
    sample_var = float(np.var(empirical_means, ddof=1))
    avg_se_sq = float(np.mean(standard_errors**2))
    tau_sq = max(1e-8, sample_var - avg_se_sq)

    # Precision-weighted shrinkage towards prior mean 0
    weights = tau_sq / (tau_sq + standard_errors**2)
    shrunken_means = weights * empirical_means

    print("--- Empirical Bayes Shrinkage ---")
    print(f"Prior Variance tau^2: {tau_sq:.8f}")
    print(f"Max Shrinkage Weight: {float(np.max(weights)):.4f}")
    print(f"Min Shrinkage Weight: {float(np.min(weights)):.4f}")
    print(f"Mean Shrunken Premium: {float(np.mean(shrunken_means)):.5f}")

    # 2. Out-of-sample decay calculation
    is_ret = rng.normal(0.0075, 0.040, size=144)
    oos_ret = rng.normal(0.0035, 0.042, size=72)

    mean_is = float(np.mean(is_ret))
    mean_oos = float(np.mean(oos_ret))
    retention_ratio = mean_oos / mean_is
    decay_ratio = 1.0 - retention_ratio

    s_is = float(np.std(is_ret, ddof=1))
    s_oos = float(np.std(oos_ret, ddof=1))
    denom = np.sqrt(s_is**2 / len(is_ret) + s_oos**2 / len(oos_ret))
    welch_t = (mean_is - mean_oos) / denom
    welch_p = float(2.0 * (1.0 - stats.norm.cdf(abs(welch_t))))

    print("--- Out-of-Sample Performance Decay ---")
    print(f"In-Sample Mean: {mean_is:.5f}")
    print(f"Out-of-Sample Mean: {mean_oos:.5f}")
    print(f"Retention Ratio: {retention_ratio:.4f}")
    print(f"Decay Ratio: {decay_ratio:.4f}")
    print(f"Welch t-stat: {welch_t:.4f} (p-val: {welch_p:.4f})")


def main() -> None:
    run_completion_pipeline()


main()
