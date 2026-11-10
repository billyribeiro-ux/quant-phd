"""Lab AP2-project-2: Project Rung 2 completion problem solution.

On the project page, the lines computing beta_hat and t_alpha are replaced with blanks (___).
This twin contains the complete solution.
"""

from __future__ import annotations

import math


def main() -> None:
    t_obs = 60
    mkt = [0.008 + 0.04 * math.sin(t * 0.3) for t in range(t_obs)]
    asset = [0.001 + 1.1 * mkt[t] + 0.02 * math.cos(t * 0.5) for t in range(t_obs)]

    mean_m = sum(mkt) / float(t_obs)
    mean_a = sum(asset) / float(t_obs)
    s_mm = sum((m - mean_m) ** 2 for m in mkt)
    s_am = sum((mkt[t] - mean_m) * (asset[t] - mean_a) for t in range(t_obs))

    beta_hat = s_am / s_mm
    alpha_hat = mean_a - beta_hat * mean_m
    residuals = [asset[t] - (alpha_hat + beta_hat * mkt[t]) for t in range(t_obs)]
    sse = sum(e * e for e in residuals)
    s2 = sse / float(t_obs - 2)
    var_alpha = s2 * (1.0 / float(t_obs) + (mean_m * mean_m) / s_mm)
    se_alpha = math.sqrt(var_alpha)
    t_alpha = alpha_hat / se_alpha

    print(f"Sample length T:   {t_obs}")
    print(f"Estimated beta:    {beta_hat:.6f}")
    print(f"Estimated alpha:   {alpha_hat:.6f}")
    print(f"Standard error se: {se_alpha:.6f}")
    print(f"t-statistic:       {t_alpha:.4f}")


main()
