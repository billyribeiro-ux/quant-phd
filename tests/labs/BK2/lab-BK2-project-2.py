"""Lab BK2-project-2: Rung 2 completed solution.

Solves the Berk-Green equilibrium completion problem: precision-weighted
Bayesian skill updating, equilibrium capacity sizing, and flow determination.
"""

from __future__ import annotations


def solve_completion_problem() -> dict[str, float]:
    prior_mean = 0.025
    prior_variance = 0.0004
    noise_variance = 0.0100
    fee_rate = 0.010
    cost_parameter = 1.5e-5
    current_aum = 200.0
    signal = 0.065
    net_return = 0.055

    # 1. Bayesian precision update
    prior_prec = 1.0 / prior_variance
    noise_prec = 1.0 / noise_variance
    post_prec = prior_prec + noise_prec
    post_variance = 1.0 / post_prec
    post_mean = (prior_prec * prior_mean + noise_prec * signal) / post_prec

    # 2. Capacity calculation
    target_capacity = max(0.0, (post_mean - fee_rate) / cost_parameter)

    # 3. Flow determination
    assets_end = max(0.0, current_aum * (1.0 + net_return))
    flow = target_capacity - assets_end

    return {
        "post_mean": post_mean,
        "post_variance": post_variance,
        "target_capacity": target_capacity,
        "assets_end": assets_end,
        "flow": flow,
    }


def main() -> None:
    res = solve_completion_problem()
    print("Project Rung 2: Completion Solution")
    print("-----------------------------------")
    print(f"Posterior Mean:     {res['post_mean']:.5f}")
    print(f"Posterior Variance: {res['post_variance']:.7f}")
    print(f"Target Capacity:    ${res['target_capacity']:,.2f}M")
    print(f"End-of-Period AUM:  ${res['assets_end']:,.2f}M")
    print(f"Net Investor Flow:  ${res['flow']:,.2f}M")


main()
