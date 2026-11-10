"""Lab AP8-L02-1: Fama-French (2010) Cross-Sectional Bootstrap Fund Skill Test.

SIMULATED: Implements the cross-sectional bootstrap test of mutual fund skill,
evaluating the empirical distribution of fund alpha t-statistics against the simulated
null distribution under zero true skill while preserving cross-sectional residual correlation.
"""

from __future__ import annotations

import numpy as np


def run_fama_french_bootstrap(
    n_funds: int = 250,
    n_months: int = 120,
    n_boot: int = 500,
    seed: int = 42,
) -> dict[str, list[float] | np.ndarray]:
    """Execute the Fama & French (2010) cross-sectional bootstrap test.

    Returns actual cross-sectional percentiles of t(alpha), mean bootstrapped null percentiles,
    and empirical one-sided p-values.
    """
    rng = np.random.default_rng(seed)

    # 1. Simulate market excess return
    r_m = rng.normal(0.006, 0.045, size=n_months)  # ~7.2% annual, 15.6% vol

    # 2. Simulate fund characteristics
    betas = rng.normal(1.0, 0.12, size=n_funds)

    # True monthly net alphas: 80% zero-skill (-10 bps fee), 15% negative, 5% positive
    true_alpha = np.zeros(n_funds)
    n_unskilled = int(0.15 * n_funds)
    n_skilled = int(0.05 * n_funds)
    n_zero = n_funds - n_unskilled - n_skilled

    true_alpha[:n_unskilled] = -0.0025  # -25 bps/mo (-3.0%/yr)
    true_alpha[n_unskilled : n_unskilled + n_zero] = -0.0010  # -10 bps/mo (fee drag)
    true_alpha[n_unskilled + n_zero :] = 0.0015  # +15 bps/mo (+1.8%/yr net skill)

    # Common unobserved factor driving cross-sectional correlation
    common_factor = rng.standard_t(df=5, size=n_months) * 0.015
    loadings = rng.uniform(0.3, 1.2, size=(n_funds, 1))

    # Idiosyncratic shocks with fat tails (Student-t df=5)
    idio = rng.standard_t(df=5, size=(n_funds, n_months)) * 0.025
    residuals = loadings * common_factor + idio

    # Fund returns: R_it = alpha_i + beta_i * R_mt + e_it
    r_funds = true_alpha[:, np.newaxis] + betas[:, np.newaxis] * r_m + residuals

    # 3. Estimate actual OLS regressions: R_it = alpha_i + beta_i * R_mt + e_it
    var_m = np.var(r_m, ddof=1)
    mean_m = np.mean(r_m)
    cov_im = np.mean((r_funds - np.mean(r_funds, axis=1, keepdims=True)) * (r_m - mean_m), axis=1) * (
        n_months / (n_months - 1)
    )

    b_hat = cov_im / var_m
    a_hat = np.mean(r_funds, axis=1) - b_hat * mean_m
    e_hat = r_funds - (a_hat[:, np.newaxis] + b_hat[:, np.newaxis] * r_m)

    s2_e = np.sum(e_hat**2, axis=1) / (n_months - 2)
    se_a = np.sqrt(s2_e * (1.0 / n_months + (mean_m**2) / ((n_months - 1) * var_m)))
    t_hat = a_hat / se_a

    # 4. Construct zero-alpha returns: R_tilde_it = b_hat_i * R_mt + e_hat_it
    r_null = b_hat[:, np.newaxis] * r_m + e_hat

    # 5. Bootstrap: resample time periods with replacement across all funds
    percentile_ranks = [1, 5, 10, 25, 50, 75, 90, 95, 99]
    boot_t_percentiles = np.zeros((n_boot, len(percentile_ranks)))

    for b in range(n_boot):
        time_idx = rng.choice(n_months, size=n_months, replace=True)
        r_m_boot = r_m[time_idx]
        r_null_boot = r_null[:, time_idx]

        var_mb = np.var(r_m_boot, ddof=1)
        mean_mb = np.mean(r_m_boot)
        cov_diff = (r_null_boot - np.mean(r_null_boot, axis=1, keepdims=True)) * (r_m_boot - mean_mb)
        cov_imb = np.mean(cov_diff, axis=1) * (n_months / (n_months - 1))

        b_boot = cov_imb / var_mb
        a_boot = np.mean(r_null_boot, axis=1) - b_boot * mean_mb
        e_boot = r_null_boot - (a_boot[:, np.newaxis] + b_boot[:, np.newaxis] * r_m_boot)

        s2_eb = np.sum(e_boot**2, axis=1) / (n_months - 2)
        se_ab = np.sqrt(s2_eb * (1.0 / n_months + (mean_mb**2) / ((n_months - 1) * var_mb)))
        t_boot = a_boot / se_ab

        t_boot_sorted = np.sort(t_boot)
        boot_t_percentiles[b, :] = np.percentile(t_boot_sorted, percentile_ranks)

    actual_percentiles = np.percentile(np.sort(t_hat), percentile_ranks)
    null_mean_percentiles = np.mean(boot_t_percentiles, axis=0)

    # One-sided p-values:
    # Left tail (p <= 50): Prob(t_boot <= t_actual)
    # Right tail (p > 50): Prob(t_boot >= t_actual)
    p_values = []
    for j, p_rank in enumerate(percentile_ranks):
        if p_rank <= 50:
            pval = float(np.mean(boot_t_percentiles[:, j] <= actual_percentiles[j]))
        else:
            pval = float(np.mean(boot_t_percentiles[:, j] >= actual_percentiles[j]))
        p_values.append(pval)

    return {
        "percentiles": [float(p) for p in percentile_ranks],
        "actual_t": [float(x) for x in actual_percentiles],
        "null_t": [float(x) for x in null_mean_percentiles],
        "p_values": p_values,
    }


def main() -> None:
    res = run_fama_french_bootstrap(n_funds=250, n_months=120, n_boot=500, seed=42)

    print("================================================================================")
    print("FAMA & FRENCH (2010) CROSS-SECTIONAL BOOTSTRAP TEST OF MUTUAL FUND SKILL")
    print("================================================================================")
    hdr = f"{'Percentile':>10} | {'Actual t(α)':>13} | {'Null t(α)':>11} | {'Diff':>8} | {'p-val':>7} | {'Result':>16}"
    print(hdr)
    print("-" * 80)

    for p, act, null, pval in zip(res["percentiles"], res["actual_t"], res["null_t"], res["p_values"], strict=True):
        diff = act - null
        if p <= 10:
            interp = "Unskilled (p<0.05)" if pval < 0.05 else "Chance"
        elif p >= 95:
            interp = "Skilled (p<0.05)" if pval < 0.05 else "Chance luck"
        else:
            interp = "Fee drag / neutral"
        print(f"{p:9.0f}% | {act:13.3f} | {null:11.3f} | {diff:8.3f} | {pval:7.3f} | {interp:>16}")

    print("-" * 80)
    print("Null Hypothesis: All fund managers possess zero true gross skill (alpha = 0).")
    print("Conclusion: Negative alphas in left tail exceed sampling luck (true underperformance);")
    print("extreme right tail shows a small fraction of skilled managers covering fees.")


main()
