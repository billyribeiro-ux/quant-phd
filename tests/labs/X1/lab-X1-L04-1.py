"""Lab X1-L04-1: Forward premium anomaly and Fama variance decomposition.

Estimates the Fama (1984) regression on simulated forward premia and verifies
Fama's necessary conditions for a negative beta: Var(p_t) > Var(E[Delta s]) and Cov(E[Delta s], p_t) < 0.
"""

from __future__ import annotations

import math
import random


def fama_decomposition(
    seed: int = 101,
    n_obs: int = 240,
    var_expected_ds: float = 0.0001,
    var_risk_premium: float = 0.0004,
    corr_ed_p: float = -0.75,
) -> dict[str, float | bool]:
    """Simulate expected depreciation and time-varying risk premium to test Fama conditions.

    Forward premium: fp_t = f_t - s_t = E_t[Delta s_{t+1}] + p_t
    Fama beta = Cov(Delta s_{t+1}, fp_t) / Var(fp_t)
              = [Var(E[Delta s]) + Cov(E[Delta s], p_t)] / Var(fp_t)
    """
    rng = random.Random(seed)

    # Covariance between expected depreciation and risk premium
    cov_ed_p = corr_ed_p * math.sqrt(var_expected_ds * var_risk_premium)

    # Variance of the forward premium fp = E[Delta s] + p
    var_fp = var_expected_ds + var_risk_premium + 2.0 * cov_ed_p

    # Theoretical Fama beta:
    beta_theoretical = (var_expected_ds + cov_ed_p) / var_fp

    # Simulate series
    sd_e = math.sqrt(var_expected_ds)
    sd_p = math.sqrt(var_risk_premium)

    fp_series: list[float] = []
    ds_series: list[float] = []

    for _ in range(n_obs):
        # Bivariate normal draw with correlation corr_ed_p
        z1 = rng.gauss(0.0, 1.0)
        z2 = rng.gauss(0.0, 1.0)
        e_ds = sd_e * z1
        p_t = sd_p * (corr_ed_p * z1 + math.sqrt(1.0 - corr_ed_p**2) * z2)

        # Forward premium
        fp = e_ds + p_t
        # Realized exchange rate change = E_t[Delta s] + rational expectations error
        realized_ds = e_ds + rng.gauss(0.0, 0.02)

        fp_series.append(fp)
        ds_series.append(realized_ds)

    # Sample regression of realized Delta s on forward premium
    mean_fp = sum(fp_series) / n_obs
    mean_ds = sum(ds_series) / n_obs

    sample_var_fp = sum((x - mean_fp) ** 2 for x in fp_series)
    sample_cov = sum((x - mean_fp) * (y - mean_ds) for x, y in zip(fp_series, ds_series, strict=True))
    beta_empirical = sample_cov / sample_var_fp

    cond1 = var_risk_premium > var_expected_ds
    cond2 = cov_ed_p < 0.0
    both_hold = cond1 and cond2

    return {
        "beta_theoretical": round(beta_theoretical, 4),
        "beta_empirical": round(beta_empirical, 4),
        "var_expected_ds": round(var_expected_ds, 6),
        "var_risk_premium": round(var_risk_premium, 6),
        "cov_ed_p": round(cov_ed_p, 6),
        "fama_condition_1": cond1,
        "fama_condition_2": cond2,
        "both_conditions_hold": both_hold,
    }


def main() -> None:
    print("Lab X1-L04-1 | Forward Premium Anomaly & Fama (1984) Decomposition")
    print("-------------------------------------------------------------------")

    res = fama_decomposition(
        seed=101,
        n_obs=240,
        var_expected_ds=0.0001,
        var_risk_premium=0.0004,
        corr_ed_p=-0.75,
    )

    print("Variance & Covariance Components:")
    print(f"  Var(E_t[Delta s_{{t+1}}]):       {res['var_expected_ds']:.6f}")
    print(f"  Var(p_t) (Risk Premium):       {res['var_risk_premium']:.6f}")
    print(f"  Cov(E_t[Delta s_{{t+1}}], p_t): {res['cov_ed_p']:.6f}")
    print("\nFama Necessary Conditions for Negative Beta (beta < 0):")
    print(f"  Condition 1: Var(p_t) > Var(E_t[Delta s]):     {res['fama_condition_1']}")
    print(f"  Condition 2: Cov(E_t[Delta s], p_t) < 0:        {res['fama_condition_2']}")
    print(f"  Both Conditions Hold:                           {res['both_conditions_hold']}")
    print("\nRegression Slope Coefficient:")
    print(f"  Theoretical Fama Beta:                         {res['beta_theoretical']:>8.4f}")
    print(f"  Empirical Estimated Beta:                      {res['beta_empirical']:>8.4f}")


main()
