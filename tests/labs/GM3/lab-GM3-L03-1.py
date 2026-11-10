"""Lab GM3-L03-1: The Fed Information Effect and Policy News Shocks.

Implements the Nakamura & Steinsson (2018) high-frequency policy news shock
via principal component analysis across the interest rate term structure,
and applies high-frequency sign restrictions to identify information shocks.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    rng = np.random.default_rng(2024)
    n_events = 120

    # 5 interest rate futures surprises in 30-min FOMC window:
    # ff1 (current month), ff2 (next month), ed2 (2Q ahead), ed3 (3Q ahead), ed4 (4Q ahead)
    # Underlying latent factors: factor 1 (policy path / level shock) + idiosyncratic noise
    latent_shock = rng.normal(0.0, 5.0, size=n_events)

    # Loadings across horizons: near contracts have smaller forward guidance loadings; further contracts larger
    loadings = np.array([0.7, 0.85, 1.0, 0.95, 0.90])
    noise_cov = 0.8 * np.eye(5)

    surprises = np.outer(latent_shock, loadings) + rng.multivariate_normal(np.zeros(5), noise_cov, size=n_events)

    # Principal Component Analysis (eigen-decomposition of sample covariance)
    surprises_centered = surprises - np.mean(surprises, axis=0)
    cov_matrix = np.cov(surprises_centered, rowvar=False)
    eigvals, eigvecs = np.linalg.eigh(cov_matrix)

    # Sort descending
    idx_sorted = np.argsort(eigvals)[::-1]
    eigvals_sorted = eigvals[idx_sorted]
    eigvecs_sorted = eigvecs[:, idx_sorted]

    var_explained_pc1 = float(eigvals_sorted[0] / np.sum(eigvals_sorted))

    # First principal component (policy news shock series)
    pc1_weights = eigvecs_sorted[:, 0]
    # Ensure positive correlation with short rate
    if pc1_weights[0] < 0:
        pc1_weights = -pc1_weights

    policy_news_shock = surprises_centered @ pc1_weights

    # High-frequency equity reaction in the same 30-min window
    # Pure monetary shocks generate negative equity reaction (discount rate channel)
    # Information shocks generate positive equity reaction (cash flow growth signal)
    # Assume 30% of announcements are dominated by information effects
    is_information = rng.binomial(1, 0.30, size=n_events)
    equity_responses_bps = np.zeros(n_events)
    for i in range(n_events):
        if is_information[i] == 1:
            # Positive co-movement: Fed hike signals economic strength
            equity_responses_bps[i] = 1.2 * policy_news_shock[i] + rng.normal(0.0, 8.0)
        else:
            # Negative co-movement: Pure policy tightening
            equity_responses_bps[i] = -2.5 * policy_news_shock[i] + rng.normal(0.0, 8.0)

    # Sign restriction classification:
    # Pure contractionary: shock > 0 and equity < 0
    # Pure expansionary: shock < 0 and equity > 0
    # Hawkish information: shock > 0 and equity > 0
    # Dovish information: shock < 0 and equity < 0
    pure_tightening = int(np.sum((policy_news_shock > 0.5) & (equity_responses_bps < -0.5)))
    pure_easing = int(np.sum((policy_news_shock < -0.5) & (equity_responses_bps > 0.5)))
    hawkish_info = int(np.sum((policy_news_shock > 0.5) & (equity_responses_bps > 0.5)))
    dovish_info = int(np.sum((policy_news_shock < -0.5) & (equity_responses_bps < -0.5)))

    corr_shock_equity = float(np.corrcoef(policy_news_shock, equity_responses_bps)[0, 1])

    print("FOMC Policy Windows Analyzed:", n_events)
    print("PC1 Variance Explained:", round(var_explained_pc1, 4))
    print("Policy News Shock Std Dev (bps):", round(float(np.std(policy_news_shock, ddof=1)), 4))
    print("Overall Shock-Equity Correlation:", round(corr_shock_equity, 4))
    print("Pure Monetary Tightening Events:", pure_tightening)
    print("Pure Monetary Easing Events:", pure_easing)
    print("Hawkish Information Effect Events:", hawkish_info)
    print("Dovish Information Effect Events:", dovish_info)


main()
