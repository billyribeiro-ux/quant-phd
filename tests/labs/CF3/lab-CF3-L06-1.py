"""CF3 lab L06-1: Shareholder rights indices: G-Index vs E-Index (Gompers et al. 2003; Bebchuk et al. 2008).

Model: Cross-sectional empirical comparison of the 24-provision G-Index (Gompers, Ishii & Metrick 2003)
versus the 6-provision entrenchment E-Index (Bebchuk, Cohen & Ferrell 2008).
Simulates cross-section of corporate governance structures and Tobin's Q to test whether
the 6 entrenchment provisions drive valuation discounts while non-entrenchment provisions add noise.
Standard library only; deterministic cross-section.
"""

from __future__ import annotations

import math
import random


def simulate_governance_panel(
    n_firms: int = 60,
    seed: int = 42,
) -> list[dict[str, float]]:
    """Simulate a cross-section of firms with 6 entrenchment and 18 non-entrenchment provisions."""
    rng = random.Random(seed)
    firms: list[dict[str, float]] = []

    # True DGP: Q = 2.40 - 0.12 * E_index + 0.0 * Other_index + noise
    true_alpha = 2.40
    true_beta_e = -0.12
    true_beta_o = 0.00  # Non-entrenchment provisions do not affect value

    for i in range(n_firms):
        # 6 core entrenchment provisions (prob ~ 0.50 each)
        e_provs = [1 if rng.random() < 0.50 else 0 for _ in range(6)]
        e_index = sum(e_provs)

        # 18 non-entrenchment provisions (prob ~ 0.40 each)
        o_provs = [1 if rng.random() < 0.40 else 0 for _ in range(18)]
        o_index = sum(o_provs)

        g_index = e_index + o_index

        noise = rng.gauss(0.0, 0.25)
        tobins_q = max(0.80, true_alpha + true_beta_e * e_index + true_beta_o * o_index + noise)

        firms.append(
            {
                "firm_id": float(i + 1),
                "e_index": float(e_index),
                "o_index": float(o_index),
                "g_index": float(g_index),
                "tobins_q": round(tobins_q, 4),
            }
        )

    return firms


def ols_bivariate(x: list[float], y: list[float]) -> dict[str, float]:
    """Bivariate OLS regression with n - 2 degrees of freedom."""
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    s_xx = sum((xi - mean_x) ** 2 for xi in x)
    s_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y, strict=True))
    s_yy = sum((yi - mean_y) ** 2 for yi in y)

    beta = s_xy / s_xx
    alpha = mean_y - beta * mean_x
    rss = sum((yi - (alpha + beta * xi)) ** 2 for xi, yi in zip(x, y, strict=True))
    s2 = rss / (n - 2)
    se_beta = math.sqrt(s2 / s_xx)
    t_stat = beta / se_beta if se_beta > 0 else 0.0
    r2 = 1.0 - (rss / s_yy) if s_yy > 0 else 0.0

    return {
        "alpha": alpha,
        "beta": beta,
        "se_beta": se_beta,
        "t_stat": t_stat,
        "r2": r2,
    }


def main() -> None:
    print("CF3 Lab L06-1: Shareholder Rights Indices: G-Index vs. E-Index")
    print("=============================================================")

    n_firms = 60
    firms = simulate_governance_panel(n_firms=n_firms, seed=777)

    e_vals = [f["e_index"] for f in firms]
    g_vals = [f["g_index"] for f in firms]
    q_vals = [f["tobins_q"] for f in firms]

    # Model 1: Tobin's Q on Bebchuk et al. (2008) E-Index (6 provisions)
    res_e = ols_bivariate(e_vals, q_vals)

    # Model 2: Tobin's Q on Gompers et al. (2003) G-Index (24 provisions)
    res_g = ols_bivariate(g_vals, q_vals)

    print(f"Sample of {n_firms} corporate issuers:")
    print(f"  E-Index range: [{min(e_vals):.0f}, {max(e_vals):.0f}], mean: {sum(e_vals) / n_firms:.2f} / 6")
    print(f"  G-Index range: [{min(g_vals):.0f}, {max(g_vals):.0f}], mean: {sum(g_vals) / n_firms:.2f} / 24")
    print(f"  Tobin's Q range: [{min(q_vals):.2f}, {max(q_vals):.2f}], mean: {sum(q_vals) / n_firms:.2f}")

    print("\nModel 1: Regressing Tobin's Q on E-Index (Bebchuk et al. 2008):")
    print("  Q_i = alpha + beta_E * E_Index_i + e_i")
    print(f"  Intercept (alpha):   {res_e['alpha']:.4f}")
    print(f"  Slope (beta_E):      {res_e['beta']:.4f} (se: {res_e['se_beta']:.4f})")
    print(f"  t-statistic:         {res_e['t_stat']:.4f}")
    print(f"  R-squared:           {res_e['r2']:.4%}")

    print("\nModel 2: Regressing Tobin's Q on Full G-Index (Gompers et al. 2003):")
    print("  Q_i = alpha + beta_G * G_Index_i + e_i")
    print(f"  Intercept (alpha):   {res_g['alpha']:.4f}")
    print(f"  Slope (beta_G):      {res_g['beta']:.4f} (se: {res_g['se_beta']:.4f})")
    print(f"  t-statistic:         {res_g['t_stat']:.4f}")
    print(f"  R-squared:           {res_g['r2']:.4%}")

    print("\nEmpirical Takeaway (Bebchuk, Cohen & Ferrell 2008):")
    t_ratio = abs(res_e["t_stat"]) / abs(res_g["t_stat"])
    print(f"  E-Index t-statistic is {t_ratio:.2f}x stronger than G-Index.")
    print("  Adding the 18 non-entrenchment provisions dilutes statistical power and attenuates the slope.")


main()
