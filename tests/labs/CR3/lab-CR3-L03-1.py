"""Lab CR3-L03-1: Excess Bond Premium Decomposition and Macroeconomic Forecasting.

SIMULATED: decomposes aggregate credit spread into default-risk compensation (S_hat)
and the Excess Bond Premium (EBP), and compares their out-of-sample predictive power
for future economic activity (Gilchrist & Zakrajšek 2012, AER).
"""

from __future__ import annotations

from typing import NamedTuple


class MacroQuarter(NamedTuple):
    q: str
    ebp: float
    s_hat: float
    term_spread: float
    growth: float


def main() -> None:
    # Stylized quarterly time series: 12 quarters covering an expansion and credit crunch
    data = [
        MacroQuarter("Q1", -35.0, 110.0, 2.2, 3.8),
        MacroQuarter("Q2", -40.0, 105.0, 2.0, 3.5),
        MacroQuarter("Q3", -25.0, 115.0, 1.6, 3.2),
        MacroQuarter("Q4", -10.0, 120.0, 1.2, 2.7),
        MacroQuarter("Q5", 15.0, 135.0, 0.5, 1.5),
        MacroQuarter("Q6", 60.0, 160.0, -0.2, -0.8),
        MacroQuarter("Q7", 110.0, 190.0, -0.6, -2.6),
        MacroQuarter("Q8", 145.0, 220.0, 0.1, -3.5),
        MacroQuarter("Q9", 90.0, 210.0, 1.4, -1.2),
        MacroQuarter("Q10", 30.0, 170.0, 2.1, 1.0),
        MacroQuarter("Q11", -15.0, 140.0, 2.4, 2.6),
        MacroQuarter("Q12", -30.0, 125.0, 2.3, 3.4),
    ]

    ebp_vals = [d.ebp for d in data]
    shat_vals = [d.s_hat for d in data]
    growth_vals = [d.growth for d in data]

    def simple_regression(x: list[float], y: list[float]) -> tuple[float, float, float]:
        mean_x = sum(x) / len(x)
        mean_y = sum(y) / len(y)
        ss_xx = sum((xi - mean_x) ** 2 for xi in x)
        ss_xy = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y, strict=False))
        ss_yy = sum((yi - mean_y) ** 2 for yi in y)
        beta = ss_xy / ss_xx if ss_xx > 0 else 0.0
        alpha = mean_y - beta * mean_x
        r2 = (ss_xy**2) / (ss_xx * ss_yy) if (ss_xx * ss_yy) > 0 else 0.0
        return alpha, beta, r2

    # Model 1: Growth on EBP
    _alpha_ebp, beta_ebp, r2_ebp = simple_regression(ebp_vals, growth_vals)

    # Model 2: Growth on S_hat (default component)
    _alpha_shat, beta_shat, r2_shat = simple_regression(shat_vals, growth_vals)

    print("Macroeconomic Forecasting: Excess Bond Premium vs Expected Default Component:")
    print("  Quarter | EBP (bp) | S_hat (bp) | Total GZ (bp) | Future 4Q GDP Growth (%)")
    print("----------+----------+------------+---------------+-------------------------")
    for d in data:
        gz_tot = d.ebp + d.s_hat
        print(
            f"    {d.q:3s}   |   {d.ebp:5.1f}  |    {d.s_hat:5.1f}   |     "
            f"{gz_tot:5.1f}     |          {d.growth:4.1f}%"
        )

    print("\nPredictive Regressions (Forward 4-Quarter Economic Growth):")
    print(f"  Model 1 (EBP only):    beta = {beta_ebp:7.4f}, R^2 = {r2_ebp * 100:4.1f}%")
    print(f"  Model 2 (S_hat only):  beta = {beta_shat:7.4f}, R^2 = {r2_shat * 100:4.1f}%")

    # In Gilchrist & Zakrajsek (2012), EBP carries substantially higher forecasting power than S_hat
    assert r2_ebp > r2_shat
    assert beta_ebp < 0.0


main()
