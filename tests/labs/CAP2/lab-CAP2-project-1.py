"""Lab CAP2-project-1: Automated evidence brief evaluation for asset pricing debate.

Demonstrates end-to-end multiple testing hurdle evaluation, Empirical Bayes
shrinkage of contested anomaly premia, out-of-sample decay testing, and
counterfactual policy divergence analysis.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def evaluate_debate_brief(
    t_stats: np.ndarray,
    num_tested: int,
    empirical_means: np.ndarray,
    standard_errors: np.ndarray,
    is_returns: np.ndarray,
    oos_returns: np.ndarray,
) -> None:
    # 1. Multiple testing hurdles (Harvey, Liu & Zhu 2016)
    alpha = 0.05
    alpha_bonf = alpha / float(num_tested)
    hurdle = float(stats.norm.ppf(1.0 - alpha_bonf / 2.0))
    bonf_sig = np.abs(t_stats) >= hurdle

    print(f"Total Universe Hypotheses Tested: {num_tested}")
    print(f"Multiple Testing t-Hurdle (alpha={alpha:.2f}): {hurdle:.4f}")
    print(f"Claims Evaluated: {len(t_stats)}")
    print(f"Claims Passing Bonferroni Hurdle: {int(np.sum(bonf_sig))}/{len(t_stats)}")

    # 2. Empirical Bayes shrinkage
    k = len(empirical_means)
    sample_var = float(np.var(empirical_means, ddof=1)) if k > 1 else float(np.mean(empirical_means**2))
    avg_se_sq = float(np.mean(standard_errors**2))
    tau_sq = max(1e-8, sample_var - avg_se_sq)

    weights = tau_sq / (tau_sq + standard_errors**2)
    shrunken_means = weights * empirical_means

    print(f"Estimated True Prior Dispersion (tau): {np.sqrt(tau_sq):.5f}")
    print(f"Average Empirical Mean: {float(np.mean(empirical_means)):.5f}")
    print(f"Average Shrunken Mean: {float(np.mean(shrunken_means)):.5f}")
    print(f"Average Shrinkage Weight (Signal-to-Total): {float(np.mean(weights)):.4f}")

    # 3. Out-of-sample decay analysis (McLean & Pontiff 2016)
    m_is = float(np.mean(is_returns))
    m_oos = float(np.mean(oos_returns))
    s_is = float(np.std(is_returns, ddof=1))
    s_oos = float(np.std(oos_returns, ddof=1))

    sr_is = m_is / s_is * np.sqrt(12.0)
    sr_oos = m_oos / s_oos * np.sqrt(12.0)
    retention = m_oos / m_is if abs(m_is) > 1e-12 else 0.0
    decay = 1.0 - retention

    denom = np.sqrt(s_is**2 / len(is_returns) + s_oos**2 / len(oos_returns))
    t_decay = (m_is - m_oos) / denom
    p_decay = 2.0 * (1.0 - stats.norm.cdf(abs(t_decay)))

    print(f"In-Sample Annualized Sharpe Ratio: {sr_is:.4f}")
    print(f"Out-of-Sample Annualized Sharpe Ratio: {sr_oos:.4f}")
    print(f"Post-Discovery Return Decay: {decay * 100.0:.2f}%")
    print(f"Welch Decay t-stat: {t_decay:.4f} (p-val: {p_decay:.4f})")


def main() -> None:
    rng = np.random.default_rng(2026)

    # Seeded synthetic brief data
    t_stats = np.array([3.82, 2.95, 2.45, 1.88, 3.21, 1.42, 2.76, 3.44])
    num_tested = 250

    empirical_means = np.array([0.0085, 0.0062, 0.0051, 0.0038, 0.0074, 0.0029])
    standard_errors = np.array([0.0022, 0.0021, 0.0025, 0.0020, 0.0023, 0.0021])

    is_returns = rng.normal(0.0080, 0.042, size=120)
    oos_returns = rng.normal(0.0042, 0.045, size=60)

    evaluate_debate_brief(t_stats, num_tested, empirical_means, standard_errors, is_returns, oos_returns)


main()
