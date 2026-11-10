"""Lab 9: Safe Asset Convenience Yield Measurement and Supply Sensitivity.

SIMULATED numbers. Standard library only.
Measures the Treasury convenience yield as the credit-stripped yield spread
between private/agency benchmarks and US Treasuries (Krishnamurthy & Vissing-Jorgensen 2012).
Evaluates convenience yield expansion under high safe-asset demand.
"""

from fractions import Fraction


class ConvenienceYieldBenchmark:
    def __init__(
        self,
        tenor: str,
        treasury_yield: Fraction,  # Annual yield (percent per year)
        private_benchmark_yield: Fraction,  # e.g. AAA corporate / Agency yield
        credit_default_spread: Fraction,  # CDS or credit risk adjustment
    ) -> None:
        self.tenor = tenor
        self.treasury_yield = treasury_yield
        self.private_yield = private_benchmark_yield
        self.credit_spread = credit_default_spread

    def compute_convenience_yield_bp(self) -> Fraction:
        """Compute the non-pecuniary convenience yield in basis points.

        Convenience Yield = (Private Benchmark - Treasury Yield - Credit Spread) * 100 bp/percent
        """
        raw_spread = self.private_yield - self.treasury_yield
        net_convenience_pct = raw_spread - self.credit_spread
        # 1 percentage point = 100 basis points
        return net_convenience_pct * Fraction(100, 1)


def simulate_supply_shock(
    base_convenience_bp: Fraction,
    debt_to_gdp_change: float,  # Change in public debt supply as % of GDP
) -> float:
    """Semi-elasticity of convenience yield with respect to Treasury supply.

    Krishnamurthy & Vissing-Jorgensen (2012) estimate that higher Treasury supply
    depresses the marginal convenience yield (downward-sloping demand for safe assets).
    """
    # Slope approx -1.2 bp per 1 percentage point increase in Debt/GDP
    slope = -1.2
    return float(base_convenience_bp) + slope * debt_to_gdp_change


def main() -> None:
    # 3 tenors: 3-month (cash/bill), 5-year, 10-year
    # All yields in percent per year (e.g. 4.25% = 425/100)
    benchmarks = [
        ConvenienceYieldBenchmark(
            tenor="3-Month",
            treasury_yield=Fraction(420, 100),  # 4.20%
            private_benchmark_yield=Fraction(465, 100),  # 4.65% (A1/P1 commercial paper)
            credit_default_spread=Fraction(5, 100),  # 0.05% (5 bp credit risk)
        ),
        ConvenienceYieldBenchmark(
            tenor="5-Year",
            treasury_yield=Fraction(380, 100),  # 3.80%
            private_benchmark_yield=Fraction(445, 100),  # 4.45% (AAA corporate)
            credit_default_spread=Fraction(25, 100),  # 0.25% (25 bp credit risk)
        ),
        ConvenienceYieldBenchmark(
            tenor="10-Year",
            treasury_yield=Fraction(400, 100),  # 4.00%
            private_benchmark_yield=Fraction(485, 100),  # 4.85% (AAA corporate)
            credit_default_spread=Fraction(35, 100),  # 0.35% (35 bp credit risk)
        ),
    ]

    print("=== Safe Asset Convenience Yield Measurement ===")
    print(f"{'Tenor':<8} | {'Treasury':<10} | {'Benchmark':<10} | {'Credit Spread':<14} | {'Convenience Yield':<18}")
    print("-" * 70)

    convenience_bps: list[Fraction] = []
    for b in benchmarks:
        cy_bp = b.compute_convenience_yield_bp()
        convenience_bps.append(cy_bp)
        ty = float(b.treasury_yield)
        py = float(b.private_yield)
        cs = float(b.credit_spread) * 100
        print(f"{b.tenor:<8} | {ty:.2f}%     | {py:.2f}%     | {cs:.0f} bp        | {float(cy_bp):.1f} bp")

    # Supply elasticity analysis on 10-year
    base_10y_cy = convenience_bps[2]
    print("\n=== Supply & Demand Sensitivity (10-Year Treasury) ===")
    print(f"Baseline Convenience Yield: {float(base_10y_cy):.1f} bp")

    # Scenario A: Treasury supply expands by +10% of GDP
    cy_supply_expand = simulate_supply_shock(base_10y_cy, debt_to_gdp_change=+10.0)
    print(f"Treasury Supply Expands (+10% Debt/GDP): Convenience Yield narrows to {cy_supply_expand:.1f} bp")

    # Scenario B: Flight-to-safety safe asset shortage (-10% supply shock / high foreign demand)
    cy_safety_scramble = simulate_supply_shock(base_10y_cy, debt_to_gdp_change=-10.0)
    print(f"Safe Asset Scramble (-10% effective supply): Convenience Yield widens to {cy_safety_scramble:.1f} bp")

    assert all(cy > 0 for cy in convenience_bps), "All convenience yields must be positive"
    assert cy_safety_scramble > float(base_10y_cy) > cy_supply_expand, (
        "Convenience yield must be downward-sloping in supply"
    )


main()
