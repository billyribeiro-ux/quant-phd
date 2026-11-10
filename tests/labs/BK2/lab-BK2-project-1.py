"""Lab BK2-project-1: Project Rung 1 - Worked example of the Berk-Green model.

Calculates single-period fund capacity, Bayesian belief updating with observation
noise, end-of-period asset value, net investor flows, and rent extraction.
"""

from __future__ import annotations


def worked_example() -> dict[str, float]:
    # Initial parameters
    mu_0 = 0.030  # 3.0% prior expected skill
    sigma_0_sq = 0.0004  # prior variance (sigma_0 = 2.0%)
    sigma_eps_sq = 0.0100  # noise variance (sigma_eps = 10.0%)
    fee_rate = 0.012  # 1.2% annual management fee (120 bps)
    lam = 2.0e-5  # scale cost parameter per million AUM
    q_0 = 100.0  # $100M initial AUM

    # 1. Capacity before observation
    q_star_0 = max(0.0, (mu_0 - fee_rate) / lam)

    # 2. Realization: manager skill = 3.5%, noise shock = +4.0%
    true_skill = 0.035
    shock = 0.040
    gross_alpha = true_skill - lam * q_0
    gross_ret = gross_alpha + shock
    net_ret = gross_ret - fee_rate
    fees_collected = fee_rate * q_0
    investor_profit = q_0 * net_ret

    # 3. Bayesian update from observed gross return
    signal = gross_ret + lam * q_0
    tau_prior = 1.0 / sigma_0_sq
    tau_noise = 1.0 / sigma_eps_sq
    tau_post = tau_prior + tau_noise
    sigma_post_sq = 1.0 / tau_post
    mu_1 = (tau_prior * mu_0 + tau_noise * signal) / tau_post

    # 4. Next period target capacity and net flow
    q_star_1 = max(0.0, (mu_1 - fee_rate) / lam)
    assets_end = max(0.0, q_0 * (1.0 + net_ret))
    net_flow = q_star_1 - assets_end

    return {
        "initial_capacity": q_star_0,
        "gross_return_pct": gross_ret * 100.0,
        "net_return_pct": net_ret * 100.0,
        "observed_signal_pct": signal * 100.0,
        "posterior_mean_pct": mu_1 * 100.0,
        "posterior_variance": sigma_post_sq,
        "new_capacity": q_star_1,
        "net_flow": net_flow,
        "fees_collected": fees_collected,
        "investor_profit": investor_profit,
    }


def main() -> None:
    res = worked_example()
    print("Project Rung 1: Berk-Green Single-Period Worked Example")
    print("------------------------------------------------------")
    print(f"Initial Prior Capacity AUM:  ${res['initial_capacity']:,.1f}M")
    print(f"Realized Gross Return:       {res['gross_return_pct']:.2f}%")
    print(f"Realized Net Return:         {res['net_return_pct']:.2f}%")
    print(f"Extracted Skill Signal:      {res['observed_signal_pct']:.2f}%")
    print(f"Updated Posterior Skill:     {res['posterior_mean_pct']:.3f}%")
    print(f"New Equilibrium Capacity:    ${res['new_capacity']:,.1f}M")
    print(f"Net Investor Flow:           ${res['net_flow']:,.2f}M")
    print(f"Manager Fees Collected:      ${res['fees_collected']:,.3f}M")
    print(f"Investor Dollar Profit:      ${res['investor_profit']:,.3f}M")


main()
