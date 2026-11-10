"""Lab F7-L02-1: Lo (2002) Autocorrelation-Adjusted Sharpe Ratio and Asymptotics.

Demonstrates the distortion of naive sqrt(12) Sharpe ratio annualization under
positive return autocorrelation, computes sample autocorrelations rho_k, evaluates
the Lo (2002) time-aggregation adjustment factor eta(q), and derives asymptotic
confidence intervals for the Sharpe ratio.
"""

from __future__ import annotations

import numpy as np
import scipy.stats


def run_lo_sharpe_analysis(seed: int = 42) -> dict[str, float]:
    """Compute naive and Lo (2002) autocorrelation-adjusted Sharpe ratios."""
    rng = np.random.default_rng(seed)
    burn_in = 60
    n_months = 240  # 20 years
    total_len = n_months + burn_in
    q_horizon = 12  # annualization horizon (12 months)

    # 1. Simulate stationary AR(1) return series with positive serial persistence:
    # r_t = c + phi * r_{t-1} + e_t
    phi_ar1 = 0.40
    innov_vol = 0.030
    target_mean = 0.008

    c_const = target_mean * (1.0 - phi_ar1)
    raw_returns = np.zeros(total_len)
    r_prev = target_mean
    for t in range(total_len):
        r_t = c_const + phi_ar1 * r_prev + rng.normal(0.0, innov_vol)
        raw_returns[t] = r_t
        r_prev = r_t

    returns = raw_returns[burn_in:]

    # 2. Sample statistics
    sample_mean = float(np.mean(returns))
    sample_std = float(np.std(returns, ddof=1))
    sr_monthly = sample_mean / sample_std

    # Naive annualization: SR_naive = sqrt(12) * SR_monthly
    sr_naive_ann = float(np.sqrt(q_horizon) * sr_monthly)

    # 3. Autocorrelation estimation: rho_k for k = 1, ..., q-1
    demeaned = returns - sample_mean
    var_denom = float(np.sum(demeaned**2))
    rho_estimates = np.zeros(q_horizon - 1)
    for k in range(1, q_horizon):
        cov_k = float(np.sum(demeaned[k:] * demeaned[:-k]))
        rho_estimates[k - 1] = cov_k / var_denom

    # 4. Lo (2002) time-aggregation correction factor eta(q):
    # eta(q) = sqrt( q / (q + 2 * sum_{k=1}^{q-1} (q - k) * rho_k) )
    cross_terms_sum = 0.0
    for k in range(1, q_horizon):
        cross_terms_sum += 2.0 * (q_horizon - k) * rho_estimates[k - 1]

    denom_var_ratio = float(q_horizon + cross_terms_sum)
    eta_q = float(np.sqrt(float(q_horizon) / denom_var_ratio))

    # Autocorrelation-adjusted annualized Sharpe ratio
    sr_adjusted_ann = eta_q * sr_naive_ann

    # 5. Asymptotic standard error of monthly Sharpe ratio under Lo (2002)
    rho_sum_kernel = float(np.sum(rho_estimates[:4]))
    hac_inflation = float(np.sqrt(max(1.0 + 2.0 * rho_sum_kernel, 0.1)))
    se_sr_iid = float(np.sqrt((1.0 + 0.5 * (sr_monthly**2)) / float(n_months)))
    se_sr_hac = se_sr_iid * hac_inflation

    # 95% Confidence interval for adjusted annualized Sharpe ratio
    z_crit = float(scipy.stats.norm.ppf(0.975))
    ci_lower = float(sr_adjusted_ann - z_crit * se_sr_hac * np.sqrt(q_horizon) * eta_q)
    ci_upper = float(sr_adjusted_ann + z_crit * se_sr_hac * np.sqrt(q_horizon) * eta_q)

    pct_overstatement = float(((sr_naive_ann / sr_adjusted_ann) - 1.0) * 100.0)

    return {
        "sample_mean_ann": round(sample_mean * 12.0 * 100.0, 2),
        "sample_vol_ann": round(sample_std * np.sqrt(12.0) * 100.0, 2),
        "rho_1": round(float(rho_estimates[0]), 4),
        "rho_2": round(float(rho_estimates[1]), 4),
        "eta_q": round(eta_q, 4),
        "sr_naive_ann": round(sr_naive_ann, 4),
        "sr_adjusted_ann": round(sr_adjusted_ann, 4),
        "pct_overstatement": round(pct_overstatement, 2),
        "ci_lower": round(ci_lower, 4),
        "ci_upper": round(ci_upper, 4),
    }


def main() -> None:
    print("Lab F7-L02-1 | Lo (2002) Autocorrelation-Adjusted Sharpe Ratio")
    print("-------------------------------------------------------------")
    res = run_lo_sharpe_analysis(seed=42)
    print(f"Sample Annualized Mean:      {res['sample_mean_ann']:.2f}% (vol {res['sample_vol_ann']:.2f}%)")
    print(f"First-Order Autocorr (rho1): {res['rho_1']:+.4f} (rho2: {res['rho_2']:+.4f})")
    print(f"Lo (2002) eta(12) Factor:    {res['eta_q']:.4f}")
    print(f"Naive Annualized Sharpe:     {res['sr_naive_ann']:.4f}")
    print(f"Lo-Adjusted Annualized SR:   {res['sr_adjusted_ann']:.4f}")
    print(f"Naive Sharpe Overstatement:  +{res['pct_overstatement']:.2f}%")
    print(f"Adjusted 95% Conf Interval:  [{res['ci_lower']:.4f}, {res['ci_upper']:.4f}]")


main()
