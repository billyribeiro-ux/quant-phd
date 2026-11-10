"""Lab F5-L05-1: Hierarchical Bayesian Shrinkage of Factor Alphas.

Implements Empirical Bayes shrinkage of cross-sectional factor alphas (Jensen,
Kelly & Pedersen 2023), estimating prior hyperparameters via marginal maximum
likelihood and demonstrating out-of-sample mean squared error reduction.
"""

from __future__ import annotations

import numpy as np
from scipy import optimize


def evaluate_bayesian_shrinkage(seed: int = 42) -> dict[str, float | int]:
    """Simulate noisy factor alphas and compute Empirical Bayes shrinkage."""
    rng = np.random.default_rng(seed)
    n_factors = 80
    n_months = 180

    # True prior distribution: mu_0 = 0.15% / mo (1.8% ann), tau = 0.20% / mo (2.4% ann)
    true_mu0 = 0.0015
    true_tau = 0.0020
    true_alphas = rng.normal(true_mu0, true_tau, size=n_factors)

    # Heterogeneous factor residual volatilities: 3% to 8% monthly
    idio_vols = rng.uniform(0.030, 0.080, size=n_factors)
    se_alpha = idio_vols / np.sqrt(n_months)

    # In-sample realized alphas
    sample_alphas = true_alphas + rng.normal(0.0, se_alpha, size=n_factors)

    # Empirical Bayes: Estimate (mu_0, tau^2) via Marginal Maximum Likelihood
    # Marginal distribution: hat{alpha}_i ~ Normal(mu_0, tau^2 + se_i^2)
    def neg_log_lik(params: np.ndarray) -> float:
        mu = params[0]
        log_tau2 = params[1]
        tau2 = np.exp(log_tau2)
        total_var = tau2 + se_alpha**2
        ll = -0.5 * np.sum(np.log(2.0 * np.pi * total_var) + ((sample_alphas - mu) ** 2) / total_var)
        return -float(ll)

    init_guess = np.array([float(np.mean(sample_alphas)), np.log(float(np.var(sample_alphas, ddof=1)))])
    opt = optimize.minimize(neg_log_lik, init_guess, method="L-BFGS-B")
    est_mu0 = float(opt.x[0])
    est_tau2 = float(np.exp(opt.x[1]))
    est_tau = float(np.sqrt(est_tau2))

    # Posterior shrinkage weight: w_i = tau^2 / (tau^2 + se_i^2)
    weights = est_tau2 / (est_tau2 + se_alpha**2)
    bayes_alphas = weights * sample_alphas + (1.0 - weights) * est_mu0

    # Convert to annualized percentage terms
    ann = 12.0 * 100.0
    mse_ols_ann = float(np.mean(((sample_alphas - true_alphas) * ann) ** 2))
    mse_bayes_ann = float(np.mean(((bayes_alphas - true_alphas) * ann) ** 2))
    mse_reduction_pct = float((1.0 - mse_bayes_ann / mse_ols_ann) * 100)

    mean_weight = float(np.mean(weights))
    min_weight = float(np.min(weights))
    max_weight = float(np.max(weights))

    return {
        "n_factors": n_factors,
        "n_months": n_months,
        "est_mu0_ann": round(est_mu0 * ann, 2),
        "est_tau_ann": round(est_tau * ann, 2),
        "mean_weight": round(mean_weight, 3),
        "min_weight": round(min_weight, 3),
        "max_weight": round(max_weight, 3),
        "mse_ols_ann": round(mse_ols_ann, 2),
        "mse_bayes_ann": round(mse_bayes_ann, 2),
        "mse_reduction_pct": round(mse_reduction_pct, 2),
    }


def main() -> None:
    print("Lab F5-L05-1 | Hierarchical Bayesian Shrinkage of Factor Alphas")
    print("-------------------------------------------------------------")
    res = evaluate_bayesian_shrinkage(seed=42)
    print(f"Sample: {res['n_factors']} cross-sectional factor alphas over {res['n_months']} months")
    print(f"Empirical Bayes Prior Mean (mu_0): {res['est_mu0_ann']:+.2f}% ann")
    print(f"Empirical Bayes Prior Std (tau):   {res['est_tau_ann']:.2f}% ann")
    print(
        f"Shrinkage Weight w_i (Signal / Total): mean {res['mean_weight']:.3f} "
        f"[range {res['min_weight']:.3f} to {res['max_weight']:.3f}]"
    )
    print(f"Sample OLS Mean Squared Error:     {res['mse_ols_ann']:.2f} (% ann)^2")
    print(f"Bayesian Shrunk MSE:               {res['mse_bayes_ann']:.2f} (% ann)^2")
    print(f"MSE Error Reduction:               {res['mse_reduction_pct']:.2f}%")


main()
