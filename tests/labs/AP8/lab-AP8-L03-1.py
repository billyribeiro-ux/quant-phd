"""Lab AP8-L03-1: Equilibrium Economics of Active Management (Berk & van Binsbergen 2015).

SIMULATED: Simulates the Berk & Green (2004) and Berk & van Binsbergen (2015) equilibrium
where competitive investors allocate capital to active funds with decreasing returns to scale,
demonstrating that net alpha converges to zero while gross value added measures true managerial skill.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class ActiveEquilibriumResult:
    corr_skill_net_alpha: float
    corr_skill_value_added: float
    mean_net_alpha: float
    mean_value_added: float
    total_value_added: float
    pct_zero_net_alpha: float
    n_active: int


def simulate_active_management_equilibrium(
    n_funds: int = 150,
    n_years: int = 30,
    b_scale: float = 0.002,  # Diseconomy parameter ($0.2% gross alpha drag per $100M AUM)
    fee: float = 0.015,  # 1.5% annual management fee
    flow_speed: float = 0.5,  # Capital allocation response speed
    seed: int = 101,
) -> ActiveEquilibriumResult:
    """Simulate fund size dynamics and evaluate net alpha vs. value added."""
    rng = np.random.default_rng(seed)

    # Manager intrinsic skill a_i ~ Uniform(0.00, 0.06) (0% to 6% annualized gross alpha at zero AUM)
    skill_a = rng.uniform(0.00, 0.06, size=n_funds)

    # Initial AUM (in millions of dollars)
    aum = rng.uniform(20.0, 100.0, size=n_funds)

    # Evolve fund AUM and returns over time
    for _ in range(n_years):
        gross_alpha = skill_a - b_scale * (aum / 100.0) + rng.normal(0.0, 0.015, size=n_funds)
        net_alpha = gross_alpha - fee

        # Capital flows respond to observed net alpha
        flow_rate = np.clip(flow_speed * (net_alpha / 0.01), -0.5, 0.8)
        aum = np.maximum(5.0, aum * (1.0 + flow_rate))

    # Final period steady state evaluation
    final_gross_alpha = skill_a - b_scale * (aum / 100.0)
    final_net_alpha = final_gross_alpha - fee
    # Dollar Value Added V_i = AUM * gross_alpha (in millions per year)
    value_added = aum * final_gross_alpha

    # Correlations (exclude funds at minimum bound)
    active = aum > 6.0
    corr_skill_net_alpha = float(np.corrcoef(skill_a[active], final_net_alpha[active])[0, 1])
    corr_skill_value_added = float(np.corrcoef(skill_a[active], value_added[active])[0, 1])

    mean_net_alpha = float(np.mean(final_net_alpha[active]))
    mean_value_added = float(np.mean(value_added[active]))
    total_value_added = float(np.sum(value_added[active]))
    pct_zero_net_alpha = float(np.mean(np.abs(final_net_alpha[active]) < 0.005) * 100.0)

    return ActiveEquilibriumResult(
        corr_skill_net_alpha=corr_skill_net_alpha,
        corr_skill_value_added=corr_skill_value_added,
        mean_net_alpha=mean_net_alpha,
        mean_value_added=mean_value_added,
        total_value_added=total_value_added,
        pct_zero_net_alpha=pct_zero_net_alpha,
        n_active=int(np.sum(active)),
    )


def main() -> None:
    res = simulate_active_management_equilibrium(n_funds=150, n_years=35, seed=101)

    print("================================================================================")
    print("EQUILIBRIUM ACTIVE MANAGEMENT: BERK & GREEN (2004) / BERK & VAN BINSBERGEN (2015)")
    print("================================================================================")
    print(f"Active Funds in Long-Run Steady State:  {res.n_active}")
    print(f"Mean Final Net Alpha (annualized):      {res.mean_net_alpha * 100:+.2f}%")
    print(f"Funds with |Net Alpha| < 50 bps:        {res.pct_zero_net_alpha:.1f}%")
    print(f"Mean Dollar Value Added per Fund:       ${res.mean_value_added:.2f}M / year")
    print(f"Total Industry Dollar Value Added:      ${res.total_value_added:.2f}M / year")
    print("-" * 80)
    print("EVALUATION OF SKILL METRICS:")
    print(f"  Corr(True Manager Skill, Net Alpha):     {res.corr_skill_net_alpha:+.4f} (Uninformative)")
    print(f"  Corr(True Manager Skill, Value Added):   {res.corr_skill_value_added:+.4f} (Highly Informative)")
    print("-" * 80)
    print("Economic Conclusion:")
    print("1. Net alpha does not measure skill: rational capital flows drive net alpha to zero.")
    print("2. Dollar value added V = AUM * gross_alpha measures skill and captures manager rents.")


main()
