"""Lab S6-L05-1: Goodman-Bacon decomposition and negative weights under staggered adoption.

Constructed example: demonstrates the Goodman-Bacon (2021) decomposition of two-way fixed effects (TWFE)
in a 3-cohort staggered adoption panel with dynamic treatment effects, showing how already-treated
units act as bad controls and receive negative contributions.
"""

from __future__ import annotations

from fractions import Fraction


def main() -> None:
    # 3 cohorts, 1 unit each, observed over 3 time periods t=1, 2, 3 (balanced panel)
    # Baseline counterfactual trend is 0 for all units
    # Cohort U (Never-treated): D = [0, 0, 0], Y = [10, 10, 10]
    # Cohort E (Early treated at t=2): D = [0, 1, 1]
    #   Treatment effect is dynamic: +2 at t=2, +8 at t=3
    #   Y = [10, 12, 18]
    # Cohort L (Late treated at t=3): D = [0, 0, 1]
    #   Treatment effect: +2 at t=3
    #   Y = [10, 10, 12]

    panel = [
        # (unit, time, y, d)
        (0, 1, Fraction(10), Fraction(0)),
        (0, 2, Fraction(10), Fraction(0)),
        (0, 3, Fraction(10), Fraction(0)),
        (1, 1, Fraction(10), Fraction(0)),
        (1, 2, Fraction(12), Fraction(1)),
        (1, 3, Fraction(18), Fraction(1)),
        (2, 1, Fraction(10), Fraction(0)),
        (2, 2, Fraction(10), Fraction(0)),
        (2, 3, Fraction(12), Fraction(1)),
    ]

    # 1. Full TWFE regression: Y_it = alpha_i + lambda_t + beta_TWFE * D_it + e_it via FWL
    n_units = Fraction(3)
    n_times = Fraction(3)
    n_obs = Fraction(len(panel))

    y_mean = sum((r[2] for r in panel), Fraction(0)) / n_obs
    d_mean = sum((r[3] for r in panel), Fraction(0)) / n_obs

    y_unit = [sum((r[2] for r in panel if r[0] == i), Fraction(0)) / n_times for i in range(3)]
    d_unit = [sum((r[3] for r in panel if r[0] == i), Fraction(0)) / n_times for i in range(3)]

    y_time = [sum((r[2] for r in panel if r[1] == t), Fraction(0)) / n_units for t in range(1, 4)]
    d_time = [sum((r[3] for r in panel if r[1] == t), Fraction(0)) / n_units for t in range(1, 4)]

    d_tilde: list[Fraction] = []
    y_tilde: list[Fraction] = []
    for u, t, y, d in panel:
        t_idx = t - 1
        d_res = d - d_unit[u] - d_time[t_idx] + d_mean
        y_res = y - y_unit[u] - y_time[t_idx] + y_mean
        d_tilde.append(d_res)
        y_tilde.append(y_res)

    var_d_tilde = sum(dt**2 for dt in d_tilde)
    cov_dy_tilde = sum(dt * yt for dt, yt in zip(d_tilde, y_tilde, strict=True))
    beta_twfe = cov_dy_tilde / var_d_tilde

    # 2. Goodman-Bacon (2021) 2x2 Sub-Estimates:
    # 2a. Early vs Never (over t=1,2,3; post is t=2,3)
    # Early change: (12 + 18)/2 - 10 = 15 - 10 = 5; Never change = 0
    beta_eu = Fraction(5, 1)

    # 2b. Late vs Never (over t=1,2,3; post is t=3)
    # Late change: 12 - (10 + 10)/2 = 12 - 10 = 2; Never change = 0
    beta_lu = Fraction(2, 1)

    # 2c. Early vs Late as clean control (over t=1,2; post is t=2)
    # Early change: 12 - 10 = 2; Late change: 10 - 10 = 0
    beta_el = Fraction(2, 1)

    # 2d. Late vs Already-Treated Early as control (over t=2,3; post is t=3)
    # Late change: 12 - 10 = 2; Early change: 18 - 12 = 6
    # beta_LE = 2 - 6 = -4 (severely negative due to growth in dynamic effect!)
    beta_le = Fraction(-4, 1)

    # 3. Goodman-Bacon exact analytical weights from Eq. (5) & (6):
    # s_EU = 1/3, s_LU = 1/3, s_EL = 1/6, s_LE = 1/6
    w_eu = Fraction(1, 3)
    w_lu = Fraction(1, 3)
    w_el = Fraction(1, 6)
    w_le = Fraction(1, 6)

    bacon_sum = w_eu * beta_eu + w_lu * beta_lu + w_el * beta_el + w_le * beta_le

    print("Goodman-Bacon TWFE Staggered Adoption Decomposition (Constructed Panel):")
    print(f"  Overall TWFE Coefficient (beta_TWFE): {beta_twfe} ({float(beta_twfe):.4f})")
    print(f"  Bacon Decomposed Weighted Sum:       {bacon_sum} ({float(bacon_sum):.4f})")
    print(f"  Exact Equivalence Check:             {beta_twfe == bacon_sum}\n")

    print("2x2 Component Decomposition:")
    print(
        f"  1. Early vs Never (clean):           estimate = {float(beta_eu):+.2f}, weight = {float(w_eu):.4f} ({w_eu})"
    )
    print(
        f"  2. Late vs Never (clean):            estimate = {float(beta_lu):+.2f}, weight = {float(w_lu):.4f} ({w_lu})"
    )
    print(
        f"  3. Early vs Late (timing pre):       estimate = {float(beta_el):+.2f}, weight = {float(w_el):.4f} ({w_el})"
    )
    le_str = f"estimate = {float(beta_le):+.2f}, weight = {float(w_le):.4f} ({w_le})"
    print(f"  4. Late vs Already-Treated (dirty):  {le_str}  <-- Dynamic bias!")
    print(f"  Sum of Weights: {w_eu + w_lu + w_el + w_le}")


main()
