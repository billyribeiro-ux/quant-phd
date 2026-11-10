"""Lab F5-project-2: Project Rung 2 Completion Problem - Multiple Testing & Shrinkage Engine.

Completed reference twin for the Project Rung 2 completion exercise. Implements
Bonferroni/Holm/BH multiple testing adjustments, Empirical Bayes prior estimation,
and double-selection orthogonalization.
"""

from __future__ import annotations

import numpy as np
from scipy import stats


def run_adjudication_subroutines(
    t_stats: np.ndarray,
    alphas: np.ndarray,
    se_alphas: np.ndarray,
    candidate: np.ndarray,
    controls: np.ndarray,
) -> dict[str, float | int]:
    """Execute key multiple testing and shrinkage subroutines.

    Completed solution for Rung 2 completion problem.
    """
    m = len(t_stats)
    t_obs = len(candidate)

    # 1. Bonferroni threshold and Holm step-down FWER
    alpha_bonf = 0.05 / float(m)
    crit_bonf = float(stats.norm.ppf(1.0 - alpha_bonf / 2.0))
    p_values = 2.0 * (1.0 - stats.norm.cdf(np.abs(t_stats)))

    sort_idx = np.argsort(p_values)
    sorted_p = p_values[sort_idx]
    holm_thresholds = 0.05 / (float(m) - np.arange(m))
    holm_passed = sorted_p <= holm_thresholds
    n_holm = int(np.argmin(holm_passed)) if not np.all(holm_passed) else m

    # 2. Empirical Bayes Shrinkage
    precisions = 1.0 / (se_alphas**2)
    mu_0 = float(np.sum(precisions * alphas) / np.sum(precisions))
    sample_var = float(np.var(alphas, ddof=1))
    mean_se2 = float(np.mean(se_alphas**2))
    tau2 = max(1e-8, sample_var - mean_se2)
    weights = tau2 / (tau2 + se_alphas**2)
    mean_weight = float(np.mean(weights))

    # 3. Orthogonalization against control factor 0
    c0 = controls[:, 0]
    x_mat = np.column_stack([np.ones(t_obs), c0])
    b_proj = np.linalg.lstsq(x_mat, candidate, rcond=None)[0]
    orth_alpha = float(b_proj[0])
    residuals = candidate - x_mat @ b_proj
    res_var = float(np.sum(residuals**2) / (t_obs - 2))
    se_orth = float(np.sqrt(res_var * np.linalg.inv(x_mat.T @ x_mat)[0, 0]))
    t_orth = float(orth_alpha / se_orth)

    return {
        "crit_bonf": round(crit_bonf, 3),
        "n_holm": n_holm,
        "prior_mu0_ann": round(mu_0 * 12 * 100, 2),
        "mean_weight": round(mean_weight, 3),
        "t_orth": round(t_orth, 2),
    }


def main() -> None:
    print("Project Rung 2 | Multiple Testing & Shrinkage Engine (Completion Solution)")
    print("--------------------------------------------------------------------------")
    rng = np.random.default_rng(42)
    t_stats = np.array([3.4, 2.2, 1.8, 0.5, 4.1, -2.5, -0.8, 1.2, 2.9, -3.1])
    alphas = rng.normal(0.002, 0.003, size=10)
    se_alphas = rng.uniform(0.001, 0.0025, size=10)
    candidate = rng.normal(0.003, 0.04, size=240)
    controls = rng.normal(0.005, 0.04, size=(240, 4))

    res = run_adjudication_subroutines(t_stats, alphas, se_alphas, candidate, controls)
    print(f"Bonferroni critical hurdle:       |t| >= {res['crit_bonf']}")
    print(f"Holm step-down discoveries:       {res['n_holm']}")
    print(f"Empirical Bayes Prior Mean:       {res['prior_mu0_ann']:+.2f}% ann")
    print(f"Mean Shrinkage Weight (Signal):   {res['mean_weight']:.3f}")
    print(f"Orthogonalized Factor t-stat:     t = {res['t_orth']:.2f}")


main()
