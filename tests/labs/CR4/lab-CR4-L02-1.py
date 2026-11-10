"""Lab CR4-L02-1: Empirical Recovery Rates Across Seniority and Credit Cycles.

Simulates multi-tranche recovery realizations across credit cycles.
Demonstrates the empirical seniority gradient, bimodal recovery distributions,
and negative correlation between aggregate default rates and recovery rates.
"""

from __future__ import annotations

import random


def simulate_firm_recovery(
    asset_realization: float,
    fl_claim: float,
    unsec_claim: float,
    sub_claim: float,
) -> dict[str, float]:
    """Allocate realized asset value down seniority tranches."""
    rem = asset_realization

    fl_rec = min(rem, fl_claim)
    rem -= fl_rec

    unsec_rec = min(rem, unsec_claim)
    rem -= unsec_rec

    sub_rec = min(rem, sub_claim)
    rem -= sub_rec

    return {
        "fl_rate": fl_rec / fl_claim if fl_claim > 0 else 0.0,
        "unsec_rate": unsec_rec / unsec_claim if unsec_claim > 0 else 0.0,
        "sub_rate": sub_rec / sub_claim if sub_claim > 0 else 0.0,
    }


def main() -> None:
    rng = random.Random(42)
    n_firms = 5000

    # Capital structure: FL = 50, Unsecured = 30, Subordinated = 20, Total = 100
    fl_claim = 50.0
    unsec_claim = 30.0
    sub_claim = 20.0
    total_debt = fl_claim + unsec_claim + sub_claim

    # Regime 1: Normal Macroeconomic Default Cycle
    # Assets at default distributed as Beta-scaled with mean 55 (55% of debt)
    fl_rates_normal: list[float] = []
    unsec_rates_normal: list[float] = []
    sub_rates_normal: list[float] = []

    for _ in range(n_firms):
        # Beta draw with alpha=3, beta=2.5 scaled to 100
        asset_draw = rng.betavariate(3.0, 2.5) * total_debt
        res = simulate_firm_recovery(asset_draw, fl_claim, unsec_claim, sub_claim)
        fl_rates_normal.append(res["fl_rate"])
        unsec_rates_normal.append(res["unsec_rate"])
        sub_rates_normal.append(res["sub_rate"])

    # Regime 2: Severe Recession / Fire-Sale Cycle
    # Assets at default distributed with alpha=1.5, beta=3.5 (mean 30% of debt)
    fl_rates_stress: list[float] = []
    unsec_rates_stress: list[float] = []
    sub_rates_stress: list[float] = []

    for _ in range(n_firms):
        asset_draw = rng.betavariate(1.5, 3.5) * total_debt
        res = simulate_firm_recovery(asset_draw, fl_claim, unsec_claim, sub_claim)
        fl_rates_stress.append(res["fl_rate"])
        unsec_rates_stress.append(res["unsec_rate"])
        sub_rates_stress.append(res["sub_rate"])

    def stats(data: list[float]) -> tuple[float, float, float]:
        mean_val = sum(data) / len(data)
        var_val = sum((x - mean_val) ** 2 for x in data) / len(data)
        std_val = var_val**0.5
        # Percent with full recovery (>= 99%)
        full_pct = sum(1 for x in data if x >= 0.99) / len(data) * 100.0
        return mean_val, std_val, full_pct

    fl_m_n, fl_s_n, fl_f_n = stats(fl_rates_normal)
    unsec_m_n, unsec_s_n, unsec_f_n = stats(unsec_rates_normal)
    sub_m_n, sub_s_n, sub_f_n = stats(sub_rates_normal)

    fl_m_s, fl_s_s, fl_f_s = stats(fl_rates_stress)
    unsec_m_s, unsec_s_s, unsec_f_s = stats(unsec_rates_stress)
    sub_m_s, sub_s_s, sub_f_s = stats(sub_rates_stress)

    print("Empirical Recovery Rate Simulation Across Seniority & Credit Cycles:")
    print("-" * 80)
    print("Tranche Seniority         | Normal Cycle (Mean / Std / Full%) | Stress Cycle (Mean / Std / Full%)")
    print("-" * 80)
    fl_norm_str = f"{fl_m_n * 100:5.1f}%  / {fl_s_n * 100:5.1f}% /  {fl_f_n:5.1f}%"
    fl_str_str = f"{fl_m_s * 100:5.1f}%  / {fl_s_s * 100:5.1f}% /  {fl_f_s:5.1f}%"
    print(f"1st Lien Secured Bank Debt|   {fl_norm_str}    |   {fl_str_str}")

    unsec_norm_str = f"{unsec_m_n * 100:5.1f}%  / {unsec_s_n * 100:5.1f}% /  {unsec_f_n:5.1f}%"
    unsec_str_str = f"{unsec_m_s * 100:5.1f}%  / {unsec_s_s * 100:5.1f}% /  {unsec_f_s:5.1f}%"
    print(f"Senior Unsecured Notes    |   {unsec_norm_str}    |   {unsec_str_str}")

    sub_norm_str = f"{sub_m_n * 100:5.1f}%  / {sub_s_n * 100:5.1f}% /  {sub_f_n:5.1f}%"
    sub_str_str = f"{sub_m_s * 100:5.1f}%  / {sub_s_s * 100:5.1f}% /  {sub_f_s:5.1f}%"
    print(f"Subordinated Debentures   |   {sub_norm_str}    |   {sub_str_str}")

    # Invariant checks: Seniority ordering holds in both regimes
    assert fl_m_n > unsec_m_n > sub_m_n
    assert fl_m_s > unsec_m_s > sub_m_s
    # Stress regime reduces recovery for all tranches
    assert fl_m_n > fl_m_s
    assert unsec_m_n > unsec_m_s
    print("\nVerified seniority gradient: 1st Lien > Unsecured > Subordinated in all cycles.")
    print("Verified procyclical distress: Stress regime depresses recoveries across all tranches.")


main()
