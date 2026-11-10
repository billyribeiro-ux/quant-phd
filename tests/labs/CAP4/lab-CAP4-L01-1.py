"""Lab CAP4-L01-1: Multiple Testing Hurdle & Empirical Bayes False Discovery Diagnostic.

Evaluates research question selection by computing Harvey-Liu-Zhu hurdle adjustments,
Benjamini-Hochberg FDR control, and empirical Bayes posterior probabilities of true discovery.
"""

from __future__ import annotations

import numpy as np
from scipy import stats  # type: ignore[import-untyped]


def main() -> None:
    # 1. Calibrated distribution of t-statistics from factor research literature
    np.random.seed(42)
    n_hypotheses = 400
    prop_true = 0.10  # 10% true signals, 90% nulls

    # Generate synthetic t-statistics: nulls ~ N(0, 1), non-nulls ~ N(3.2, 1)
    is_true = np.random.rand(n_hypotheses) < prop_true
    t_stats = np.zeros(n_hypotheses)
    t_stats[~is_true] = np.random.normal(0.0, 1.0, size=int(np.sum(~is_true)))
    t_stats[is_true] = np.random.normal(3.2, 1.0, size=int(np.sum(is_true)))

    # 2. Two-tailed p-values
    p_values = 2.0 * (1.0 - stats.norm.cdf(np.abs(t_stats)))

    # 3. Multiple testing hurdles
    # Classical unadjusted hurdle (alpha = 0.05)
    unadjusted_hurdle = float(stats.norm.ppf(1.0 - 0.05 / 2.0))
    bonferroni_alpha = 0.05 / n_hypotheses
    bonferroni_hurdle = float(stats.norm.ppf(1.0 - bonferroni_alpha / 2.0))

    # Harvey-Liu-Zhu empirical hurdle for cross-sectional anomalies (~ 3.0)
    hlz_hurdle = 3.00

    # 4. Benjamini-Hochberg False Discovery Rate (FDR = 0.05)
    sorted_indices = np.argsort(p_values)
    sorted_p = p_values[sorted_indices]
    bh_threshold = (np.arange(1, n_hypotheses + 1) / n_hypotheses) * 0.05
    significant_bh = sorted_p <= bh_threshold
    if np.any(significant_bh):
        max_idx = int(np.max(np.where(significant_bh)[0]))
        bh_discoveries = max_idx + 1
        bh_cutoff_t = float(np.abs(t_stats[sorted_indices[max_idx]]))
    else:
        bh_discoveries = 0
        bh_cutoff_t = bonferroni_hurdle

    # 5. Empirical Bayes posterior probability for a discovery with t = 2.8 vs t = 3.5
    def posterior_prob_true(t_val: float) -> float:
        f_null = float(stats.norm.pdf(t_val, 0.0, 1.0))
        f_alt = float(stats.norm.pdf(t_val, 3.2, 1.0))
        num = prop_true * f_alt
        denom = num + (1.0 - prop_true) * f_null
        return float(num / denom)

    post_t28 = posterior_prob_true(2.8)
    post_t35 = posterior_prob_true(3.5)

    print(f"Total Hypotheses Tested: {n_hypotheses}")
    print(f"Unadjusted Hurdle (p=0.05): {unadjusted_hurdle:.4f}")
    print(f"Bonferroni Hurdle: {bonferroni_hurdle:.4f}")
    print(f"Harvey-Liu-Zhu Hurdle: {hlz_hurdle:.2f}")
    print(f"Benjamini-Hochberg Discoveries: {bh_discoveries}")
    print(f"BH Effective Hurdle t: {bh_cutoff_t:.4f}")
    print(f"Posterior P(True | t=2.8): {post_t28:.4f}")
    print(f"Posterior P(True | t=3.5): {post_t35:.4f}")


main()
