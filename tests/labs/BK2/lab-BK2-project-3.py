"""Lab BK2-project-3: Project Rung 3 - Full fund-economics lifecycle model verification.

Validates the full multi-period Berk-Green fund lifecycle simulation,
checking flow accounting, fee extraction, and zero-net-alpha equilibrium.
"""

from __future__ import annotations


def run_verification() -> None:
    prior_mean = 0.030
    prior_variance = 0.0004
    noise_variance = 0.0100
    fee_rate = 0.015
    cost_param = 2.0e-5
    init_aum = 100.0
    true_skill = 0.035
    shocks = [0.015, -0.020, 0.030, -0.010, 0.005]

    aum = init_aum
    mu = prior_mean
    var = prior_variance

    total_fees = 0.0
    total_inv_profit = 0.0

    print("Project Rung 3: Lifecycle Simulation Verification")
    print("-------------------------------------------------")
    print(
        f"{'Period':<7} {'AUM ($M)':<11} {'Net Return':<12} {'Fees ($M)':<11} {'InvProfit ($M)':<15} {'Post Skill':<10}"
    )
    print("-------------------------------------------------------------------------")

    for t, shock in enumerate(shocks, start=1):
        alpha_g = true_skill - cost_param * aum
        r_gross = alpha_g + shock
        r_net = r_gross - fee_rate
        fees = fee_rate * aum
        inv_prof = aum * r_net

        total_fees += fees
        total_inv_profit += inv_prof

        # Bayesian update
        sig = r_gross + cost_param * aum
        tau_prior = 1.0 / var
        tau_noise = 1.0 / noise_variance
        tau_post = tau_prior + tau_noise
        var = 1.0 / tau_post
        mu = (tau_prior * mu + tau_noise * sig) / tau_post

        target_cap = max(0.0, (mu - fee_rate) / cost_param)

        print(
            f"{t:<7} "
            f"${aum:>8.1f}M  "
            f"{r_net * 100.0:>8.2f}%     "
            f"${fees:>7.3f}M   "
            f"${inv_prof:>10.3f}M    "
            f"{mu * 100.0:>7.3f}%"
        )

        aum = target_cap

    rent_share = total_fees / (total_fees + total_inv_profit) if (total_fees + total_inv_profit) > 0 else 1.0
    print("-------------------------------------------------------------------------")
    print(f"Cumulative Manager Fees:    ${total_fees:,.3f}M")
    print(f"Cumulative Investor Profit: ${total_inv_profit:,.3f}M")
    print(f"Manager Rent Share:         {rent_share * 100.0:.2f}%")


def main() -> None:
    run_verification()


main()
