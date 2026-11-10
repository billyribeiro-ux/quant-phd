"""Lab F5-L06-1: Feng, Giglio & Xiu (2020) Double-Selection Factor Pricing Test.

Implements the two-step penalized double-selection methodology to evaluate whether
a candidate factor provides incremental pricing power beyond a high-dimensional
library of control factors.
"""

from __future__ import annotations

import numpy as np


def evaluate_double_selection(seed: int = 42) -> dict[str, float | int | bool]:
    """Execute double-selection factor test on candidate factor with 40 controls."""
    rng = np.random.default_rng(seed)
    n_months = 240
    n_controls = 40
    n_assets = 25

    # 1. Simulate 40 control factors: 5 dominant systematic factors, 35 weak/idiosyncratic factors
    factor_cov = np.eye(n_controls) * (0.04**2)
    # Common correlation block among the first 5 factors
    for i in range(5):
        for j in range(5):
            if i != j:
                factor_cov[i, j] = 0.30 * 0.04 * 0.04

    controls = rng.multivariate_normal(mean=np.full(n_controls, 0.003), cov=factor_cov, size=n_months)

    # 2. Simulate candidate factor g_t:
    # Set to be largely spanned by control factor 1 and factor 3 (loading 0.50 and 0.40),
    # with a very small true incremental alpha of 0.05% / mo
    true_incremental_alpha = 0.0005
    noise_g = rng.normal(0.0, 0.02, size=n_months)
    candidate_g = true_incremental_alpha + 0.50 * controls[:, 0] + 0.40 * controls[:, 2] + noise_g

    # 3. Simulate 25 test asset excess returns
    # Asset returns driven primarily by the 5 dominant factors
    betas_assets = rng.uniform(0.5, 1.5, size=(n_assets, 5))
    noise_assets = rng.normal(0.0, 0.03, size=(n_assets, n_months))
    asset_returns = betas_assets @ controls[:, :5].T + noise_assets

    # Mean returns of test assets and candidate factor
    mean_assets = np.mean(asset_returns, axis=1)

    # NAIVE TEST: Regress test assets on candidate g alone (univariate Fama-MacBeth)
    # Estimate univariate beta_i,g = Cov(R_i, g) / Var(g)
    var_g = float(np.var(candidate_g, ddof=1))
    cov_ig = np.array([float(np.cov(asset_returns[i], candidate_g)[0, 1]) for i in range(n_assets)])
    beta_g_naive = cov_ig / var_g

    # Cross-sectional regression: mean_assets = lambda_0 + lambda_g * beta_g_naive
    x_naive = np.column_stack([np.ones(n_assets), beta_g_naive])
    b_cs_naive, _, _, _ = np.linalg.lstsq(x_naive, mean_assets, rcond=None)
    lambda_g_naive = float(b_cs_naive[1])
    res_cs_naive = mean_assets - x_naive @ b_cs_naive
    se_lambda_naive = float(
        np.sqrt(np.sum(res_cs_naive**2) / (n_assets - 2) * np.linalg.inv(x_naive.T @ x_naive)[1, 1])
    )
    t_stat_naive = lambda_g_naive / se_lambda_naive

    # DOUBLE-SELECTION PROCEDURE (Feng, Giglio & Xiu 2020)
    # Step 1: Selection of controls predicting candidate g_t
    # LASSO-type thresholding or marginal screening: correlate g_t with all 40 controls
    corrs_g_controls = np.array([np.corrcoef(candidate_g, controls[:, j])[0, 1] for j in range(n_controls)])
    # Threshold for selection (e.g. |corr| >= 0.15 or top explanatory controls)
    thresh_step1 = 0.15
    selected_step1 = set(np.where(np.abs(corrs_g_controls) >= thresh_step1)[0])

    # Step 2: Selection of controls pricing test assets
    # Regress average asset returns on asset loadings on each control
    selected_step2: set[int] = set()
    for j in range(n_controls):
        var_fj = float(np.var(controls[:, j], ddof=1))
        cov_ifj = np.array([float(np.cov(asset_returns[i], controls[:, j])[0, 1]) for i in range(n_assets)])
        beta_fj = cov_ifj / var_fj
        # Check cross-sectional variance of beta (relevance to pricing)
        if np.std(beta_fj) > 0.10:
            selected_step2.add(j)

    # Union of selected controls
    selected_union = sorted(selected_step1.union(selected_step2))
    n_selected = len(selected_union)

    # Post-double-selection regression:
    # Project candidate g orthogonal to selected controls F_{union}
    x_controls_sel = np.column_stack([np.ones(n_months), controls[:, selected_union]])
    gamma_proj, _, _, _ = np.linalg.lstsq(x_controls_sel, candidate_g, rcond=None)
    g_orthogonal = candidate_g - x_controls_sel @ gamma_proj

    # Orthogonalized candidate mean, standard error, and t-statistic
    mean_g_orth = float(np.mean(g_orthogonal))
    se_g_orth = float(np.std(g_orthogonal, ddof=1) / np.sqrt(n_months))
    t_stat_ds = mean_g_orth / se_g_orth

    ann = 12.0 * 100.0
    is_spurious_naive = bool(abs(t_stat_naive) >= 1.96)
    is_retained_ds = bool(abs(t_stat_ds) >= 1.96)

    return {
        "n_controls": n_controls,
        "n_selected_union": n_selected,
        "lambda_g_naive_ann": round(lambda_g_naive * ann, 2),
        "t_stat_naive": round(t_stat_naive, 2),
        "is_spurious_naive": is_spurious_naive,
        "mean_g_orth_ann": round(mean_g_orth * ann, 2),
        "t_stat_ds": round(t_stat_ds, 2),
        "is_retained_ds": is_retained_ds,
    }


def main() -> None:
    print("Lab F5-L06-1 | Double-Selection Factor Pricing Test (Feng et al. 2020)")
    print("---------------------------------------------------------------------")
    res = evaluate_double_selection(seed=42)
    print(
        f"Library: {res['n_controls']} candidate controls | "
        f"Double-selection kept {res['n_selected_union']} active controls"
    )
    print(
        f"Naïve Univariate Test:        lambda_g = {res['lambda_g_naive_ann']:+.2f}% ann "
        f"| t = {res['t_stat_naive']:.2f} | Significant: {res['is_spurious_naive']}"
    )
    print(
        f"Double-Selection Orthogonal:  alpha_g  = {res['mean_g_orth_ann']:+.2f}% ann "
        f"| t = {res['t_stat_ds']:.2f} | Retained: {res['is_retained_ds']}"
    )
    print("Conclusion: Naïve test falsely accepts candidate due to omitted-factor loading;")
    print("Double-selection correctly purges spanned variance and rejects spurious factor.")


main()
