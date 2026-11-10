"""Lab BK2-L05-1: Berk-Green equilibrium convergence and flow-performance dynamics.

Demonstrates the rational active management equilibrium: a skilled manager
attracts inflows following high performance until decreasing returns to scale
drive expected net investor alpha to zero, while manager fee revenue expands.
"""

from __future__ import annotations


def simulate_berk_green_convergence(
    skill: float,
    fee_rate: float,
    cost_parameter: float,
    initial_aum: float,
    periods: int,
) -> list[dict[str, float]]:
    """Simulate fund growth, net alpha, and manager fees toward equilibrium capacity."""
    target_capacity = (skill - fee_rate) / cost_parameter
    aum = initial_aum
    history: list[dict[str, float]] = []

    for t in range(1, periods + 1):
        gross_alpha = skill - cost_parameter * aum
        net_alpha = gross_alpha - fee_rate
        fees = fee_rate * aum

        # Flow adjustment toward capacity: partial adjustment in real flows (half-life of 1 period)
        # Flow brings AUM to capacity in rational equilibrium
        flow = target_capacity - aum * (1.0 + net_alpha)
        next_aum = target_capacity

        history.append(
            {
                "period": float(t),
                "aum": aum,
                "gross_alpha_pct": gross_alpha * 100.0,
                "net_alpha_pct": net_alpha * 100.0,
                "fees_millions": fees,
                "net_flow_millions": flow,
                "capacity": target_capacity,
            }
        )
        aum = next_aum

    return history


def main() -> None:
    true_skill = 0.040  # 4.0% annualized skill
    fee_rate = 0.015  # 1.5% management fee
    cost_param = 2.5e-5  # cost per million AUM
    start_aum = 50.0  # $50M initial launch AUM
    periods = 5

    history = simulate_berk_green_convergence(true_skill, fee_rate, cost_param, start_aum, periods)
    target_cap = (true_skill - fee_rate) / cost_param

    print("Berk-Green Active Management Equilibrium Convergence")
    print("----------------------------------------------------")
    print(f"Manager Skill: {true_skill * 100.0:.1f}% | Fee: {fee_rate * 100.0:.2f}% | Scale Cost: {cost_param:.1e}")
    print(f"Equilibrium Target Capacity: ${target_cap:,.1f} Million")
    print("-------------------------------------------------------------------------")
    print(f"{'Period':<7} {'AUM ($M)':<11} {'Gross Alpha':<13} {'Net Alpha':<12} {'Fees ($M)':<11} {'Flow ($M)':<10}")
    print("-------------------------------------------------------------------------")
    for r in history:
        print(
            f"{int(r['period']):<7} "
            f"${r['aum']:>8.1f}M  "
            f"{r['gross_alpha_pct']:>8.3f}%     "
            f"{r['net_alpha_pct']:>7.3f}%    "
            f"${r['fees_millions']:>7.3f}M   "
            f"${r['net_flow_millions']:>8.2f}M"
        )
    print("-------------------------------------------------------------------------")


main()
