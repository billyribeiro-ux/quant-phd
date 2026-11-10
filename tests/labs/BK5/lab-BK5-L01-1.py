"""Lab L01-1: Lifecycle human capital valuation and Merton financial equity glidepath.

Demonstrates the decay of non-tradable human capital over working life (ages 25 to 65)
and the resulting optimal financial equity share under an unconstrained total wealth target of 60%.
Standard library only. All inputs are SIMULATED.
"""


def compute_human_capital(salary: float, growth: float, discount: float, remaining_years: int) -> float:
    """Compute present value of remaining labor earnings."""
    pv = 0.0
    current = salary
    for t in range(1, remaining_years + 1):
        pv += current / ((1.0 + discount) ** t)
        current *= 1.0 + growth
    return pv


def main() -> None:
    initial_salary = 100_000.0  # dollars
    salary_growth = 0.015  # 1.5% real growth
    human_capital_discount = 0.035  # 3.5% discount rate (bond-like labor income)
    target_total_equity_share = 0.60  # Merton optimal share of (F + H)

    # Simulated financial wealth trajectory from age 25 to 65
    # Assuming annual savings and investment compounding
    milestones = [25, 35, 45, 55, 65]
    financial_wealth_map = {
        25: 50_000.0,
        35: 250_000.0,
        45: 650_000.0,
        55: 1_350_000.0,
        65: 2_400_000.0,
    }

    for age in milestones:
        remaining_years = 65 - age
        salary_at_age = initial_salary * ((1.0 + salary_growth) ** (age - 25))
        hc = compute_human_capital(salary_at_age, salary_growth, human_capital_discount, remaining_years)
        fw = financial_wealth_map[age]
        total_wealth = fw + hc

        # Desired equity dollars = target_total_equity_share * total_wealth
        desired_equity_dollars = target_total_equity_share * total_wealth
        # Unconstrained share of financial wealth: alpha = desired_equity_dollars / fw
        unconstrained_equity_share = desired_equity_dollars / fw
        # Constrained equity share cannot exceed 100% without margin leverage
        constrained_equity_share = min(1.0, unconstrained_equity_share)

        print(
            f"age {age:2d} | salary {round(salary_at_age):6d} | "
            f"human capital {round(hc):7d} | financial wealth {round(fw):7d} | "
            f"unconstrained equity {unconstrained_equity_share:5.3f} | "
            f"effective equity {constrained_equity_share:5.3f}"
        )


main()
