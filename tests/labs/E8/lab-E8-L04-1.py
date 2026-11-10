"""Lab 4: The Impossible Trinity (Trilemma) Policy Triad Verification.

SIMULATED numbers. Standard library only.
Verifies the impossible trinity: fixed exchange rate, free capital mobility, and monetary policy autonomy
cannot hold simultaneously. Evaluates the policy wedge across the three classic corners.
"""

from fractions import Fraction


class TrilemmaRegime:
    def __init__(
        self,
        name: str,
        fixed_exchange_rate: bool,
        free_capital_mobility: bool,
        monetary_autonomy: bool,
    ) -> None:
        self.name = name
        self.fixed_fx = fixed_exchange_rate
        self.free_cap = free_capital_mobility
        self.autonomy = monetary_autonomy

    def evaluate(
        self,
        target_rate: Fraction,
        world_rate: Fraction,
    ) -> dict[str, Fraction | str]:
        """Evaluate resulting policy rate, expected depreciation, and capital control wedge."""
        if self.fixed_fx and self.free_cap:
            # Peg + Open Capital: Must import world interest rate
            actual_rate = world_rate
            expected_deprec = Fraction(0, 1)
            capital_wedge = Fraction(0, 1)
            autonomy_loss = abs(target_rate - actual_rate)
        elif not self.fixed_fx and self.free_cap:
            # Floating + Open Capital: Independent rate, FX absorbs differential via UIP
            actual_rate = target_rate
            expected_deprec = actual_rate - world_rate
            capital_wedge = Fraction(0, 1)
            autonomy_loss = Fraction(0, 1)
        elif self.fixed_fx and not self.free_cap:
            # Peg + Autonomy: Capital controls break the parity link
            actual_rate = target_rate
            expected_deprec = Fraction(0, 1)
            capital_wedge = abs(actual_rate - (world_rate + expected_deprec))
            autonomy_loss = Fraction(0, 1)
        else:
            # Closed economy or degenerate corner
            actual_rate = target_rate
            expected_deprec = Fraction(0, 1)
            capital_wedge = Fraction(0, 1)
            autonomy_loss = Fraction(0, 1)

        return {
            "regime": self.name,
            "policy_rate": actual_rate,
            "expected_deprec": expected_deprec,
            "capital_wedge": capital_wedge,
            "autonomy_loss": autonomy_loss,
        }


def test_impossible_triad(
    target_rate: Fraction,
    world_rate: Fraction,
) -> Fraction:
    """Demonstrate that claiming all 3 simultaneously creates an arbitrage inconsistency."""
    # If a policymaker claims:
    # 1. Fixed FX: Delta e = 0
    # 2. Free capital: i = i* + Delta e
    # 3. Monetary autonomy: i = target_rate != world_rate
    # Then inconsistency wedge = |target_rate - (world_rate + 0)|
    return abs(target_rate - world_rate)


def main() -> None:
    # World rate = 2.0%, Domestic target policy rate = 5.0%
    i_world = Fraction(2, 100)
    i_target = Fraction(5, 100)

    regimes = [
        TrilemmaRegime("Regime 1: Hard Peg (e.g. Currency Board / Eurozone)", True, True, False),
        TrilemmaRegime("Regime 2: Floating Exchange Rate (e.g. US, UK, Japan)", False, True, True),
        TrilemmaRegime("Regime 3: Capital Controls (e.g. Bretton Woods)", True, False, True),
    ]

    print("=== The Impossible Trinity (Trilemma) Evaluation ===")
    print(f"World Rate (i*):          {float(i_world) * 100:.1f}%")
    print(f"Domestic Target Rate (i): {float(i_target) * 100:.1f}%\n")

    for reg in regimes:
        res = reg.evaluate(i_target, i_world)
        print(f"--- {res['regime']} ---")
        print(f"  Implemented Policy Rate: {float(res['policy_rate']) * 100:.2f}%")
        print(f"  Expected FX Depreciation: {float(res['expected_deprec']) * 100:+.2f}%")
        print(f"  Required Capital Wedge:   {float(res['capital_wedge']) * 10000:.0f} bp")
        print(f"  Target Autonomy Gap:      {float(res['autonomy_loss']) * 100:.2f}%\n")

    contradiction_wedge = test_impossible_triad(i_target, i_world)
    print("=== Impossibility Proof ===")
    print(f"Contradiction Wedge if all 3 claimed: {float(contradiction_wedge) * 10000:.0f} bp")
    print("Under open capital and fixed FX, the policy rate MUST equal the world rate.")

    assert contradiction_wedge == Fraction(3, 100), "Contradiction wedge must be 300 bp"


main()
