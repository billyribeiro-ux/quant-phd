"""Lab E7-L10-1: The Natural Rate of Interest (r-star) and Post-Pandemic Inflation Decomposition.

Part 1: Holston, Laubach, and Williams (2017) state-space relationship:
   r*_t = g_t + z_t
   where g_t is trend productivity growth and z_t captures persistent non-growth factors
   (demographics, safe asset demand).

Part 2: Bernanke & Blanchard (2025) structural decomposition of the 2021-2023 inflation surge:
   Decomposes headline CPI inflation into energy price shocks, supply bottlenecks/shortages,
   and labor market tightness (v/u).
"""

from __future__ import annotations


def calculate_hlw_natural_rate(
    trend_growth_g: float,
    time_preference_z: float,
) -> float:
    """Calculate natural real rate r* = g + z per Holston, Laubach, and Williams (2017)."""
    return trend_growth_g + time_preference_z


def bernanke_blanchard_inflation_decomposition(
    initial_inflation: float,
    energy_price_growth: float,
    shortage_index: float,
    labor_tightness_vu: float,  # vacancies / unemployed ratio
    beta_energy: float = 0.08,
    beta_shortage: float = 0.15,
    beta_labor: float = 0.65,
) -> dict[str, float]:
    """Decompose headline inflation surge into energy, supply bottlenecks, and labor market tightness."""
    contrib_energy = beta_energy * energy_price_growth
    contrib_shortage = beta_shortage * shortage_index
    contrib_labor = beta_labor * max(0.0, labor_tightness_vu - 1.0)  # tightness above balanced ratio 1.0

    total_predicted = initial_inflation + contrib_energy + contrib_shortage + contrib_labor

    return {
        "baseline_inflation": initial_inflation,
        "energy_contribution": contrib_energy,
        "shortage_contribution": contrib_shortage,
        "labor_tightness_contribution": contrib_labor,
        "total_predicted_inflation": total_predicted,
    }


def main() -> None:
    # Part 1: Holston-Laubach-Williams (2017) Secular Decline in r*
    # 1970s vs 2010s comparison
    r_star_1975 = calculate_hlw_natural_rate(trend_growth_g=2.80, time_preference_z=0.70)
    r_star_2019 = calculate_hlw_natural_rate(trend_growth_g=1.10, time_preference_z=-0.60)

    print("Holston, Laubach & Williams (2017) Natural Rate (r*) Trends:")
    print(f"  1970s r*: {r_star_1975:.2f}% (trend growth g = 2.8%, persistent factor z = +0.7%)")
    print(f"  2019  r*: {r_star_2019:.2f}% (trend growth g = 1.1%, persistent factor z = -0.6%)")
    print(f"  Secular decline in r*: {r_star_2019 - r_star_1975:.2f} percentage points")

    # Part 2: Bernanke & Blanchard (2025) 2021-2023 Inflation Surge Decomposition
    # Calibration for peak US inflation in 2022 (CPI ~ 8.5%)
    decomp_2022 = bernanke_blanchard_inflation_decomposition(
        initial_inflation=2.0,  # 2% pre-pandemic anchor
        energy_price_growth=35.0,  # +35% energy price spike
        shortage_index=16.0,  # supply chain bottleneck index
        labor_tightness_vu=1.90,  # historic peak of 1.9 vacancies per unemployed worker
    )

    print("\nBernanke & Blanchard (2025) Pandemic-Era Inflation Surge Decomposition:")
    print(f"  Pre-pandemic anchor:        {decomp_2022['baseline_inflation']:.2f}%")
    print(f"  Energy commodity shock:     +{decomp_2022['energy_contribution']:.2f}%")
    print(f"  Supply chain shortages:     +{decomp_2022['shortage_contribution']:.2f}%")
    print(f"  Labor market tightness v/u: +{decomp_2022['labor_tightness_contribution']:.2f}%")
    print(f"  Total predicted inflation:   {decomp_2022['total_predicted_inflation']:.2f}%")


main()
