"""Lab F7-L03-1: Return Smoothing Dynamics and Volatility Suppression.

Simulates latent true economic returns and reported smoothed returns under
a Getmansky, Lo & Makarov (2004) moving average smoothing model, verifying
the theoretical variance reduction ratio xi = sum theta_j^2, the inflation
of reported Sharpe ratios, and the induced serial autocorrelation structure.
"""

from __future__ import annotations

import numpy as np


def run_return_smoothing_simulation(seed: int = 42) -> dict[str, float]:
    """Simulate true vs reported smoothed returns and evaluate distortions."""
    rng = np.random.default_rng(seed)
    n_months = 240
    burn_in = 24
    total_months = n_months + burn_in

    # 1. True economic parameters (unobserved latent asset return)
    # Annualized true mean = 9.6% (0.8% / mo), Annualized true vol = 18.0% (5.196% / mo)
    true_mean_mo = 0.0080
    true_vol_mo = 0.05196

    # 2. Getmansky-Lo-Makarov (2004) MA(2) smoothing weights:
    # theta = [0.55, 0.30, 0.15], sum(theta) = 1.0
    theta = np.array([0.55, 0.30, 0.15])
    k_lags = len(theta) - 1

    # Theoretical variance reduction ratio (Herfindahl concentration index):
    # xi = sum_{j=0}^k theta_j^2
    xi_theoretical = float(np.sum(theta**2))

    # Theoretical autocorrelations:
    # gamma_0 = sigma*^2 * (theta_0^2 + theta_1^2 + theta_2^2)
    # gamma_1 = sigma*^2 * (theta_0*theta_1 + theta_1*theta_2)
    # gamma_2 = sigma*^2 * (theta_0*theta_2)
    gamma_0 = xi_theoretical
    gamma_1 = float(theta[0] * theta[1] + theta[1] * theta[2])
    gamma_2 = float(theta[0] * theta[2])
    rho_1_theoretical = gamma_1 / gamma_0
    rho_2_theoretical = gamma_2 / gamma_0

    # 3. Simulate true latent returns R_t^* ~ i.i.d. Normal(mu*, sigma*^2)
    r_true_all = rng.normal(true_mean_mo, true_vol_mo, size=total_months + k_lags)

    # 4. Generate reported smoothed returns R_t = sum_{j=0}^k theta_j * R_{t-j}^*
    r_reported_all = np.zeros(total_months)
    for t in range(total_months):
        # R_t = theta_0 * R_t^* + theta_1 * R_{t-1}^* + theta_2 * R_{t-2}^*
        r_reported_all[t] = theta[0] * r_true_all[t + 2] + theta[1] * r_true_all[t + 1] + theta[2] * r_true_all[t]

    # Discard burn-in
    r_true = r_true_all[burn_in + 2 :]
    r_reported = r_reported_all[burn_in:]

    # 5. Empirical sample moments
    var_true = float(np.var(r_true, ddof=1))
    var_reported = float(np.var(r_reported, ddof=1))
    empirical_variance_ratio = var_reported / var_true

    vol_true_ann = float(np.std(r_true, ddof=1) * np.sqrt(12.0) * 100.0)
    vol_reported_ann = float(np.std(r_reported, ddof=1) * np.sqrt(12.0) * 100.0)

    mean_true_ann = float(np.mean(r_true) * 12.0 * 100.0)
    mean_reported_ann = float(np.mean(r_reported) * 12.0 * 100.0)

    sr_true_ann = float((np.mean(r_true) / np.std(r_true, ddof=1)) * np.sqrt(12.0))
    sr_reported_ann = float((np.mean(r_reported) / np.std(r_reported, ddof=1)) * np.sqrt(12.0))
    sr_inflation_pct = float(((sr_reported_ann / sr_true_ann) - 1.0) * 100.0)

    # Empirical sample autocorrelations of reported returns
    demeaned = r_reported - np.mean(r_reported)
    denom = float(np.sum(demeaned**2))
    rho_1_empirical = float(np.sum(demeaned[1:] * demeaned[:-1]) / denom)
    rho_2_empirical = float(np.sum(demeaned[2:] * demeaned[:-2]) / denom)

    return {
        "xi_theoretical": round(xi_theoretical, 4),
        "empirical_var_ratio": round(empirical_variance_ratio, 4),
        "vol_true_ann": round(vol_true_ann, 2),
        "vol_reported_ann": round(vol_reported_ann, 2),
        "mean_true_ann": round(mean_true_ann, 2),
        "mean_reported_ann": round(mean_reported_ann, 2),
        "sr_true_ann": round(sr_true_ann, 4),
        "sr_reported_ann": round(sr_reported_ann, 4),
        "sr_inflation_pct": round(sr_inflation_pct, 2),
        "rho_1_theo": round(rho_1_theoretical, 4),
        "rho_1_emp": round(rho_1_empirical, 4),
        "rho_2_theo": round(rho_2_theoretical, 4),
        "rho_2_emp": round(rho_2_empirical, 4),
    }


def main() -> None:
    print("Lab F7-L03-1 | Return Smoothing Dynamics and Volatility Suppression")
    print("------------------------------------------------------------------")
    res = run_return_smoothing_simulation(seed=42)
    print(f"Theoretical Variance Ratio (xi): {res['xi_theoretical']:.4f}")
    print(f"Empirical Variance Ratio:        {res['empirical_var_ratio']:.4f}")
    print(f"Annualized True Volatility:      {res['vol_true_ann']:.2f}%")
    suppression_pct = 100.0 - (res["vol_reported_ann"] / res["vol_true_ann"]) * 100.0
    print(f"Annualized Reported Volatility:  {res['vol_reported_ann']:.2f}% (Suppressed by {suppression_pct:.1f}%)")
    print(f"Annualized True Sharpe Ratio:    {res['sr_true_ann']:.4f}")
    print(f"Annualized Reported Sharpe:      {res['sr_reported_ann']:.4f} (+{res['sr_inflation_pct']:.1f}% inflation)")
    print(f"Autocorrelation lag 1 (theo/emp):{res['rho_1_theo']:.4f} / {res['rho_1_emp']:.4f}")
    print(f"Autocorrelation lag 2 (theo/emp):{res['rho_2_theo']:.4f} / {res['rho_2_emp']:.4f}")


main()
