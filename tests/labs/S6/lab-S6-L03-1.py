"""Lab S6-L03-1: Finite-sample bias of Two-Stage Least Squares under weak instruments.

SIMULATED: evaluates Monte Carlo finite-sample bias of 2SLS / IV toward OLS
as first-stage instrument strength varies from strong to near-zero.
"""

from __future__ import annotations

import math
import random


def run_mc_trial(rng: random.Random, n: int, gamma: float, beta_true: float) -> tuple[float, float, float]:
    """Single replication: returns (ols_beta, iv_beta, first_stage_f)."""
    # Exogenous instrument Z ~ N(0, 1)
    z = [rng.gauss(0.0, 1.0) for _ in range(n)]

    # Confounder U ~ N(0, 1) correlated with error terms
    u = [rng.gauss(0.0, 1.0) for _ in range(n)]

    # First stage: D = gamma * Z + 0.8 * U + v
    d = [gamma * z[i] + 0.8 * u[i] + rng.gauss(0.0, 0.6) for i in range(n)]

    # Structural equation: Y = beta * D + U + eps (so Cov(D, eps_total) = 0.8 > 0)
    y = [beta_true * d[i] + u[i] + rng.gauss(0.0, 0.6) for i in range(n)]

    # Sample means
    z_bar = sum(z) / n
    d_bar = sum(d) / n
    y_bar = sum(y) / n

    # First stage regression of D on Z: D = pi_0 + pi_1 * Z + e
    ss_z = sum((zi - z_bar) ** 2 for zi in z)
    sp_zd = sum((zi - z_bar) * (di - d_bar) for zi, di in zip(z, d, strict=True))
    pi_1 = sp_zd / ss_z
    pi_0 = d_bar - pi_1 * z_bar
    ss_resid_fs = sum((di - (pi_0 + pi_1 * zi)) ** 2 for zi, di in zip(z, d, strict=True))
    var_resid_fs = ss_resid_fs / (n - 2)
    # First stage F-statistic for H_0: pi_1 = 0
    f_stat = (pi_1**2 * ss_z) / var_resid_fs

    # OLS of Y on D
    ss_d = sum((di - d_bar) ** 2 for di in d)
    sp_dy = sum((di - d_bar) * (yi - y_bar) for di, yi in zip(d, y, strict=True))
    b_ols = sp_dy / ss_d

    # IV / 2SLS: Cov(Y, Z) / Cov(D, Z)
    sp_zy = sum((zi - z_bar) * (yi - y_bar) for zi, yi in zip(z, y, strict=True))
    b_iv = sp_zy / sp_zd if abs(sp_zd) > 1e-12 else float("nan")

    return b_ols, b_iv, f_stat


def main() -> None:
    rng = random.Random(2024)
    n = 250
    reps = 600
    beta_true = 2.00

    gammas = [0.80, 0.30, 0.08]
    labels = ["Strong (gamma=0.80)", "Moderate (gamma=0.30)", "Weak (gamma=0.08)"]

    print("Weak Instrument Finite-Sample Bias Evaluation (SIMULATED):")
    print(f"  Sample size N={n}, Monte Carlo replications M={reps}")
    print(f"  True causal beta: {beta_true:.4f}\n")

    for gamma, label in zip(gammas, labels, strict=True):
        ols_list: list[float] = []
        iv_list: list[float] = []
        f_list: list[float] = []

        for _ in range(reps):
            b_ols, b_iv, f_stat = run_mc_trial(rng, n, gamma, beta_true)
            if not math.isnan(b_iv) and abs(b_iv) < 50.0:  # trim extreme Cauchy tail outliers
                ols_list.append(b_ols)
                iv_list.append(b_iv)
                f_list.append(f_stat)

        mean_ols = sum(ols_list) / len(ols_list)
        mean_iv = sum(iv_list) / len(iv_list)
        mean_f = sum(f_list) / len(f_list)
        bias_iv = mean_iv - beta_true

        print(f"Regime: {label}")
        print(f"  Average first-stage F-statistic: {mean_f:.2f}")
        print(f"  Average OLS estimate:            {mean_ols:.4f} (bias: {mean_ols - beta_true:+.4f})")
        print(f"  Average 2SLS estimate:          {mean_iv:.4f} (bias: {bias_iv:+.4f})")
        print(f"  Median 2SLS estimate:           {sorted(iv_list)[len(iv_list) // 2]:.4f}\n")


main()
