"""CF9 lab L01-1: Corporate Hedging Theory - Convex Taxes and Distress Costs.

Demonstrates the Smith-Stulz (1985) corporate hedging theorem:
Under perfect capital markets (linear payoffs, no tax asymmetry, zero bankruptcy costs),
corporate hedging preserves expected shareholder wealth (hedging irrelevance).
Under convex corporate tax schedules (progressive rates or non-refundable tax losses)
or deadweight financial distress costs, corporate risk reduction strictly enhances post-tax firm value.
Standard library only; deterministic execution.
"""

from __future__ import annotations

from statistics import NormalDist


def progressive_tax_liability(pretax_income: float) -> float:
    """Compute corporate tax liability under a convex progressive rate schedule:

    - 0% on income <= 0 (no tax refund on losses)
    - 15% on income in (0, 50]
    - 30% on income > 50
    """
    if pretax_income <= 0.0:
        return 0.0
    if pretax_income <= 50.0:
        return 0.15 * pretax_income
    return 0.15 * 50.0 + 0.30 * (pretax_income - 50.0)


def financial_distress_cost(pretax_income: float, debt_service: float, distress_loss: float) -> float:
    """Compute deadweight bankruptcy / distress cost if cash flow falls below debt obligations."""
    return distress_loss if pretax_income < debt_service else 0.0


def evaluate_hedging_policies(
    mu_cf: float,
    sigma_cf: float,
    debt_service: float,
    distress_loss: float,
    n_states: int = 100_000,
) -> dict[str, float]:
    """Compare unhedged versus perfectly hedged firm value across stochastic cash flow states."""
    dist = NormalDist(mu=0.0, sigma=1.0)
    probs = [(i + 0.5) / n_states for i in range(n_states)]
    z_scores = [dist.inv_cdf(p) for p in probs]

    unhedged_cf = [mu_cf + sigma_cf * z for z in z_scores]
    hedged_cf = [mu_cf] * n_states

    # 1. Frictionless benchmark: linear flat tax (25%) with full symmetric loss offset
    tau_flat = 0.25
    unhedged_tax_linear = [tau_flat * x for x in unhedged_cf]
    hedged_tax_linear = [tau_flat * x for x in hedged_cf]
    exp_linear_tax_unhedged = sum(unhedged_tax_linear) / n_states
    exp_linear_tax_hedged = sum(hedged_tax_linear) / n_states

    # 2. Convex progressive tax schedule (Smith & Stulz 1985)
    unhedged_tax_convex = [progressive_tax_liability(x) for x in unhedged_cf]
    hedged_tax_convex = [progressive_tax_liability(x) for x in hedged_cf]
    exp_convex_tax_unhedged = sum(unhedged_tax_convex) / n_states
    exp_convex_tax_hedged = sum(hedged_tax_convex) / n_states
    tax_shield_gain = exp_convex_tax_unhedged - exp_convex_tax_hedged

    # 3. Financial distress costs
    unhedged_distress = [financial_distress_cost(x, debt_service, distress_loss) for x in unhedged_cf]
    hedged_distress = [financial_distress_cost(x, debt_service, distress_loss) for x in hedged_cf]
    exp_distress_unhedged = sum(unhedged_distress) / n_states
    exp_distress_hedged = sum(hedged_distress) / n_states
    distress_shield_gain = exp_distress_unhedged - exp_distress_hedged

    # Total net expected cash flow to investors (after convex tax and distress)
    net_cf_unhedged = mu_cf - exp_convex_tax_unhedged - exp_distress_unhedged
    net_cf_hedged = mu_cf - exp_convex_tax_hedged - exp_distress_hedged
    total_value_added = net_cf_hedged - net_cf_unhedged

    # Analytical default probability
    z_default = (debt_service - mu_cf) / sigma_cf
    prob_default_unhedged = dist.cdf(z_default)

    return {
        "mu_cf": mu_cf,
        "sigma_cf": sigma_cf,
        "exp_linear_tax_unhedged": exp_linear_tax_unhedged,
        "exp_linear_tax_hedged": exp_linear_tax_hedged,
        "exp_convex_tax_unhedged": exp_convex_tax_unhedged,
        "exp_convex_tax_hedged": exp_convex_tax_hedged,
        "tax_shield_gain": tax_shield_gain,
        "prob_default_unhedged": prob_default_unhedged,
        "exp_distress_unhedged": exp_distress_unhedged,
        "exp_distress_hedged": exp_distress_hedged,
        "distress_shield_gain": distress_shield_gain,
        "net_cf_unhedged": net_cf_unhedged,
        "net_cf_hedged": net_cf_hedged,
        "total_value_added": total_value_added,
    }


def main() -> None:
    print("CF9 Lab L01-1: Corporate Hedging Theory (Smith & Stulz 1985)")
    print("==========================================================")

    # Parameters: Volatile firm with expected pretax cash flow $80M +/- $40M
    mu = 80.0
    sigma = 40.0
    debt = 30.0
    distress_loss = 25.0

    results = evaluate_hedging_policies(
        mu_cf=mu,
        sigma_cf=sigma,
        debt_service=debt,
        distress_loss=distress_loss,
    )

    print("1. Frictionless Benchmark (Linear Flat 25% Tax, No Default Costs):")
    print(f"   Unhedged expected tax:  ${results['exp_linear_tax_unhedged']:,.2f}M")
    print(f"   Hedged expected tax:    ${results['exp_linear_tax_hedged']:,.2f}M")
    linear_tax_diff = abs(results["exp_linear_tax_unhedged"] - results["exp_linear_tax_hedged"])
    print(f"   Tax difference:         ${linear_tax_diff:,.4f}M (Hedging Irrelevance: {linear_tax_diff < 1e-4})")

    print("\n2. Asymmetric Convex Tax Regime (0% / 15% / 30%):")
    print(f"   Unhedged expected tax:  ${results['exp_convex_tax_unhedged']:,.2f}M")
    print(f"   Hedged expected tax:    ${results['exp_convex_tax_hedged']:,.2f}M")
    print(f"   Hedging tax savings:    ${results['tax_shield_gain']:,.2f}M (Jensen's Inequality)")

    print("\n3. Financial Distress Avoidance:")
    print(f"   Debt obligation:        ${debt:,.2f}M")
    print(f"   Unhedged default prob:  {results['prob_default_unhedged']:.2%}")
    print(f"   Unhedged distress cost: ${results['exp_distress_unhedged']:,.2f}M")
    print(f"   Hedged distress cost:   ${results['exp_distress_hedged']:,.2f}M")
    print(f"   Distress cost savings:  ${results['distress_shield_gain']:,.2f}M")

    print("\n4. Net Firm Value Impact:")
    print(f"   Net cash flow unhedged: ${results['net_cf_unhedged']:,.2f}M")
    print(f"   Net cash flow hedged:   ${results['net_cf_hedged']:,.2f}M")
    pct_gain = results["total_value_added"] / mu
    print(f"   Total Value Created:    ${results['total_value_added']:,.2f}M ({pct_gain:.2%} of E[CF])")


main()
