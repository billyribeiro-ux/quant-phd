"""Lab F5-L02-1: Publication Bias and Anomaly Alpha Decay.

Models the publication filter in empirical finance, measures in-sample vs.
post-publication alpha decay (McLean & Pontiff 2016), and detects funnel plot
asymmetry via Egger regressions.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def evaluate_publication_bias(seed: int = 42) -> dict[str, float | int]:
    """Simulate anomaly publication selection and post-publication decay."""
    rng = np.random.default_rng(seed)
    n_candidates = 300
    t1_is_months = 180
    t2_oos_months = 120

    # True underlying latent annualized alphas drawn from Half-Normal/Exponential
    # with mean ~ 2.4% (0.2% / mo) and vol ~ 15% (4.33% / mo)
    true_alpha_mo = rng.exponential(scale=0.0020, size=n_candidates)
    vol_mo = rng.uniform(0.030, 0.060, size=n_candidates)

    # In-sample realized returns
    is_returns = np.zeros(n_candidates)
    is_se = vol_mo / np.sqrt(t1_is_months)
    for i in range(n_candidates):
        sample = rng.normal(true_alpha_mo[i], vol_mo[i], size=t1_is_months)
        is_returns[i] = float(np.mean(sample))

    is_t_stats = is_returns / is_se

    # Publication filter: only publish if in-sample t >= 2.00
    pub_mask = is_t_stats >= 2.00
    n_published = int(np.sum(pub_mask))

    pub_is_returns = is_returns[pub_mask]
    pub_is_t = is_t_stats[pub_mask]
    pub_is_se = is_se[pub_mask]
    pub_true_alpha = true_alpha_mo[pub_mask]
    pub_vol = vol_mo[pub_mask]

    # Post-publication returns: subject to both statistical mean-reversion
    # AND arbitrage capital inflow decaying true alpha by ~30%
    arbitrage_decay_factor = 0.70
    oos_returns = np.zeros(n_published)
    for j in range(n_published):
        post_alpha = pub_true_alpha[j] * arbitrage_decay_factor
        sample_oos = rng.normal(post_alpha, pub_vol[j], size=t2_oos_months)
        oos_returns[j] = float(np.mean(sample_oos))

    # Annualized return percentages
    mean_is_ann = float(np.mean(pub_is_returns) * 12 * 100)
    mean_oos_ann = float(np.mean(oos_returns) * 12 * 100)
    mean_true_ann = float(np.mean(pub_true_alpha) * 12 * 100)

    # Anomaly decay fraction: 1 - R_oos / R_is
    decay_pct = float((1.0 - mean_oos_ann / mean_is_ann) * 100)

    # Statistical bias component: (R_is - True) / R_is
    stat_bias_pct = float(((mean_is_ann - mean_true_ann) / mean_is_ann) * 100)

    # Egger regression test for funnel asymmetry on published set:
    # t_i = beta_0 + beta_1 * (1 / SE_i) + e_i
    precision = 1.0 / pub_is_se
    x_mat = np.column_stack([np.ones_like(precision), precision])
    beta, _res, _, _ = np.linalg.lstsq(x_mat, pub_is_t, rcond=None)
    egger_intercept = float(beta[0])
    egger_slope = float(beta[1])

    # Residual standard error and intercept t-stat
    res_var = float(np.sum((pub_is_t - x_mat @ beta) ** 2) / (n_published - 2))
    cov_beta = res_var * np.linalg.inv(x_mat.T @ x_mat)
    se_intercept = float(np.sqrt(cov_beta[0, 0]))
    t_egger = egger_intercept / se_intercept
    p_egger = float(2.0 * (1.0 - stats.t.cdf(np.abs(t_egger), df=n_published - 2)))

    return {
        "n_candidates": n_candidates,
        "n_published": n_published,
        "mean_is_ann": round(mean_is_ann, 2),
        "mean_oos_ann": round(mean_oos_ann, 2),
        "mean_true_ann": round(mean_true_ann, 2),
        "decay_pct": round(decay_pct, 2),
        "stat_bias_pct": round(stat_bias_pct, 2),
        "egger_intercept": round(egger_intercept, 3),
        "egger_slope": round(egger_slope, 4),
        "t_egger": round(t_egger, 2),
        "p_egger": round(p_egger, 4),
    }


def main() -> None:
    print("Lab F5-L02-1 | Publication Bias and Anomaly Alpha Decay")
    print("------------------------------------------------------")
    res = evaluate_publication_bias(seed=42)
    print(f"Candidates tested: {res['n_candidates']} | Published (t >= 2.0): {res['n_published']}")
    print(f"In-sample published alpha:     {res['mean_is_ann']:.2f}% per year")
    print(f"Post-publication alpha:        {res['mean_oos_ann']:.2f}% per year (True: {res['mean_true_ann']:.2f}%)")
    print(f"Total post-publication decay:  {res['decay_pct']:.2f}%")
    print(f"In-sample selection bias:      {res['stat_bias_pct']:.2f}% of in-sample alpha")
    print(
        f"Egger funnel asymmetry:        intercept = {res['egger_intercept']:+.3f} "
        f"| t = {res['t_egger']:.2f} | p = {res['p_egger']:.4f}"
    )


main()
