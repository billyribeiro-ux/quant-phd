"""Lab AP2-project-1: Project Rung 1 worked example.

Annotated run of the core CAPM testing tasks on a SIMULATED 3-asset panel (T = 60).
Demonstrates:
(1) Computing GMV portfolio weights;
(2) Estimating time-series Jensen regression for one asset (alpha, beta, t-statistic);
(3) Evaluating the cross-sectional SML pricing residual.
"""

from __future__ import annotations

import math
from fractions import Fraction


def invert_3x3(mat: list[list[Fraction]]) -> list[list[Fraction]]:
    """Invert 3x3 matrix using exact row elimination."""
    n = 3
    aug = [[mat[i][j] for j in range(n)] + [Fraction(1 if i == k else 0) for k in range(n)] for i in range(n)]
    for i in range(n):
        p = aug[i][i]
        for j in range(2 * n):
            aug[i][j] /= p
        for r in range(n):
            if r != i:
                f = aug[r][i]
                for j in range(2 * n):
                    aug[r][j] -= f * aug[i][j]
    return [[aug[i][n + j] for j in range(n)] for i in range(n)]


def main() -> None:
    # SIMULATED parameters for 3 assets
    cov = [
        [Fraction(5, 1000), Fraction(2, 1000), Fraction(1, 1000)],
        [Fraction(2, 1000), Fraction(6, 1000), Fraction(2, 1000)],
        [Fraction(1, 1000), Fraction(2, 1000), Fraction(7, 1000)],
    ]
    iota = [Fraction(1, 1), Fraction(1, 1), Fraction(1, 1)]

    # Step 1: GMV weights: minimize variance subject to weights summing to 1
    # Why: The GMV is the unique portfolio on the efficient frontier with zero sensitivity to expected returns.
    inv_cov = invert_3x3(cov)
    inv_iota = [sum((inv_cov[i][j] * iota[j] for j in range(3)), Fraction(0, 1)) for i in range(3)]
    a_scalar = sum(inv_iota, Fraction(0, 1))
    w_gmv = [inv_iota[i] / a_scalar for i in range(3)]

    print(f"Step 1 (GMV weights): [{w_gmv[0]}, {w_gmv[1]}, {w_gmv[2]}]")
    print(f"GMV weights sum: {sum(w_gmv, Fraction(0, 1))}")

    # Step 2: Time-series Jensen regression on a seeded panel (T = 60)
    # Why: Jensen's alpha tests whether individual assets earn abnormal returns beyond their systematic market risk.
    # Deterministic sample (T = 60)
    t_obs = 60
    mkt = [0.01 + 0.035 * math.sin(t * 0.4) for t in range(t_obs)]
    # Asset 1 excess returns: true alpha = 0.0015, true beta = 1.2
    asset_1 = [0.0015 + 1.2 * mkt[t] + 0.015 * math.cos(t * 0.7) for t in range(t_obs)]

    mean_m = sum(mkt) / float(t_obs)
    mean_a = sum(asset_1) / float(t_obs)
    s_mm = sum((m - mean_m) ** 2 for m in mkt)
    s_am = sum((mkt[t] - mean_m) * (asset_1[t] - mean_a) for t in range(t_obs))

    beta_hat = s_am / s_mm
    alpha_hat = mean_a - beta_hat * mean_m
    residuals = [asset_1[t] - (alpha_hat + beta_hat * mkt[t]) for t in range(t_obs)]
    sse = sum(e * e for e in residuals)
    s2 = sse / float(t_obs - 2)
    var_alpha = s2 * (1.0 / float(t_obs) + (mean_m * mean_m) / s_mm)
    se_alpha = math.sqrt(var_alpha)
    t_alpha = alpha_hat / se_alpha

    print(f"Step 2 (Jensen OLS): alpha={alpha_hat:.6f}, beta={beta_hat:.6f}, se={se_alpha:.6f}, t={t_alpha:.4f}")

    # Step 3: Security Market Line residual
    # Why: The SML residual measures cross-sectional deviation from the theoretical equilibrium pricing line.
    sml_slope = mean_m
    sml_residual = mean_a - beta_hat * sml_slope
    print(f"Step 3 (SML residual): {sml_residual:.6f}")


main()
