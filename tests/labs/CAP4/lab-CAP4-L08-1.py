"""Lab CAP4-L08-1: Manuscript Statistical Articulation & Table Integrity Diagnostic.

Evaluates academic manuscript engineering by verifying mathematical articulation across
regression tables, degrees-of-freedom consistency, t-statistic matching (t = beta / se),
and covariance matrix positive-definiteness.
"""

from __future__ import annotations

import numpy as np


def main() -> None:
    # 1. Candidate manuscript regression table data (6 models)
    # Columns: [Model, Beta, Standard Error, t-stat, R^2, N_obs, df_resid]
    models = ["Model 1", "Model 2", "Model 3", "Model 4", "Model 5", "Model 6"]
    betas = np.array([0.450, 0.380, 0.520, 0.410, 0.490, 0.360])
    ses = np.array([0.090, 0.095, 0.104, 0.082, 0.098, 0.075])
    reported_ts = np.array([5.00, 4.00, 5.00, 5.00, 5.00, 4.80])
    r_squareds = np.array([0.12, 0.18, 0.22, 0.29, 0.34, 0.39])
    n_obs = 250
    k_params = np.array([2, 3, 4, 5, 6, 7])

    # 2. Articulation audits
    # Check 1: t = beta / se
    calculated_ts = betas / ses
    t_diffs = np.abs(reported_ts - calculated_ts)
    max_t_diff = float(np.max(t_diffs))
    t_articulation_pass = bool(max_t_diff < 0.05)  # Within rounding tolerance

    # Check 2: Degrees of freedom articulation df = N - K
    calculated_dfs = n_obs - k_params
    df_consistency = bool(np.all(calculated_dfs > 0))

    # Check 3: R^2 weakly monotonic with added regressors
    r2_monotonic = bool(np.all(np.diff(r_squareds) >= 0.0))

    # 3. Residual covariance matrix positive-definiteness audit
    np.random.seed(42)
    residuals_sample = np.random.normal(0.0, 0.05, size=(n_obs, len(models)))
    cov_resid = (residuals_sample.T @ residuals_sample) / (n_obs - 1)
    eigenvalues = np.linalg.eigvalsh(cov_resid)
    min_eig = float(np.min(eigenvalues))
    is_positive_definite = bool(min_eig > 0.0)

    print(f"Total Table Models Audited: {len(models)}")
    print(f"Maximum t-Statistic Rounding Discrepancy: {max_t_diff:.4f}")
    print(f"t-Statistic Articulation Valid: {t_articulation_pass}")
    print(f"Degrees of Freedom Consistent: {df_consistency}")
    print(f"Residual Degrees of Freedom Range: [{np.min(calculated_dfs)}, {np.max(calculated_dfs)}]")
    print(f"R-Squared Monotonicity Preserved: {r2_monotonic}")
    print(f"Residual Covariance Minimum Eigenvalue: {min_eig:.6f}")
    print(f"Covariance Positive-Definite: {is_positive_definite}")


main()
