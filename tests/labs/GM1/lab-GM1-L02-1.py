"""Lab GM1-L02-1: Stock-Watson Dynamic Factor Extraction in State Space.

Estimates a static dynamic factor model via principal components on a 30-variable
macroeconomic panel (Stock & Watson 2002), fits a VAR(1) transition equation on the
latent factors, and verifies factor orthogonality and transition matrix stability.
"""

from __future__ import annotations

import numpy as np


def extract_factors_and_fit_var(panel: np.ndarray, n_factors: int = 2) -> dict[str, np.ndarray | float | bool]:
    """Extract static principal component factors and fit VAR(1) state space transition."""
    t_obs, _ = panel.shape

    # 1. Standardize columns
    means = np.mean(panel, axis=0)
    stds = np.std(panel, axis=0, ddof=1)
    x_std = (panel - means) / stds

    # 2. Covariance matrix and spectral decomposition
    cov = (x_std.T @ x_std) / float(t_obs)
    eigvals, eigvecs = np.linalg.eigh(cov)

    # Sort descending
    sort_idx = np.argsort(eigvals)[::-1]
    eigvals = eigvals[sort_idx]
    eigvecs = eigvecs[:, sort_idx]

    total_var = float(np.sum(eigvals))
    explained_ratio = eigvals[:n_factors] / total_var

    # 3. Factor loadings and static factors
    loadings = eigvecs[:, :n_factors]
    factors = x_std @ loadings  # Shape (T, r)

    # Factor sample covariance
    factor_cov = (factors.T @ factors) / float(t_obs)

    # 4. VAR(1) transition: F_t = A F_{t-1} + u_t
    f_curr = factors[1:]
    f_prev = factors[:-1]
    trans_a, _, _, _ = np.linalg.lstsq(f_prev, f_curr, rcond=None)
    mat_a = trans_a.T  # Shape (r, r)

    # Transition stability: spectral radius
    eigenvalues_a = np.linalg.eigvals(mat_a)
    spectral_radius = float(np.max(np.abs(eigenvalues_a)))
    is_stable = bool(spectral_radius < 1.0)

    # Residual covariance Q
    resids = f_curr - f_prev @ trans_a
    q_cov = (resids.T @ resids) / float(len(resids) - 1)

    return {
        "eigenvalues": eigvals[:5],
        "explained_ratio": explained_ratio,
        "factor_cov": factor_cov,
        "mat_a": mat_a,
        "spectral_radius": spectral_radius,
        "is_stable": is_stable,
        "q_cov": q_cov,
    }


def main() -> None:
    print("GM1 Lab L02-1: Dynamic Factor Model Estimation in State Space [SIMULATED]")
    print("=========================================================================")

    rng = np.random.default_rng(101)
    t_obs = 240  # 20 years of monthly data
    n_series = 30  # 30 macro indicators (production, labor, prices, credit, orders)
    n_factors = 2

    # Simulate true 2-factor latent macro dynamics:
    # Factor 1: Real activity (persistent cycle)
    # Factor 2: Nominal / price-rates pressure
    true_factors = np.zeros((t_obs, n_factors), dtype=np.float64)
    true_a = np.array([[0.75, 0.04], [-0.08, 0.65]], dtype=np.float64)
    q_true = np.array([[0.30, 0.02], [0.02, 0.25]], dtype=np.float64)
    chol_q = np.linalg.cholesky(q_true)

    for t in range(1, t_obs):
        true_factors[t] = true_a @ true_factors[t - 1] + chol_q @ rng.standard_normal(n_factors)

    # Factor loadings: series 0-14 load heavily on factor 1 (real), series 15-29 on factor 2 (nominal)
    true_loadings = np.zeros((n_series, n_factors), dtype=np.float64)
    true_loadings[:15, 0] = rng.uniform(0.5, 0.9, size=15)
    true_loadings[:15, 1] = rng.uniform(-0.3, 0.3, size=15)
    true_loadings[15:, 0] = rng.uniform(-0.2, 0.4, size=15)
    true_loadings[15:, 1] = rng.uniform(0.6, 0.95, size=15)

    # Idiosyncratic noise
    idiosyncratic_noise = rng.normal(0.0, 0.45, size=(t_obs, n_series))
    raw_panel = true_factors @ true_loadings.T + idiosyncratic_noise

    res = extract_factors_and_fit_var(raw_panel, n_factors=n_factors)

    print(f"Panel dimensions: T = {t_obs} observations, N = {n_series} variables")
    print(f"Number of extracted static factors: {n_factors}")
    print("-------------------------------------------------------------------------")
    print("Top 5 Eigenvalues of Standardized Panel Covariance:")
    eigs = res["eigenvalues"]
    assert isinstance(eigs, np.ndarray)
    for i, val in enumerate(eigs):
        print(f"  Eigenvalue {i + 1}: {float(val):6.4f}")

    ratios = res["explained_ratio"]
    assert isinstance(ratios, np.ndarray)
    print(f"Variance explained by Factor 1: {float(ratios[0]) * 100:5.2f}%")
    print(f"Variance explained by Factor 2: {float(ratios[1]) * 100:5.2f}%")
    print(f"Cumulative Variance (r=2):     {float(np.sum(ratios)) * 100:5.2f}%")
    print("-------------------------------------------------------------------------")

    fcov = res["factor_cov"]
    assert isinstance(fcov, np.ndarray)
    fcov_clean = np.where(np.abs(fcov) < 1e-12, 0.0, fcov)
    print("Factor Sample Covariance Matrix (Orthogonality check F'F / T):")
    print(f"  [[{fcov_clean[0, 0]:6.4f}, {fcov_clean[0, 1]:6.4f}],")
    print(f"   [{fcov_clean[1, 0]:6.4f}, {fcov_clean[1, 1]:6.4f}]]")
    assert abs(fcov[0, 1]) < 1e-12, "Sample factors must be strictly orthogonal"
    print("Factor orthogonality confirmed: True")
    print("-------------------------------------------------------------------------")

    mat_a = res["mat_a"]
    assert isinstance(mat_a, np.ndarray)
    print("Estimated VAR(1) State Transition Matrix A:")
    print(f"  Row 1: [{mat_a[0, 0]:6.4f}, {mat_a[0, 1]:6.4f}]")
    print(f"  Row 2: [{mat_a[1, 0]:6.4f}, {mat_a[1, 1]:6.4f}]")
    print(f"Spectral radius |lambda_max|:   {float(res['spectral_radius']):.4f}")
    print(f"State space system is stable:   {res['is_stable']}")


main()
